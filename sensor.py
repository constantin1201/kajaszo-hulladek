from __future__ import annotations

from datetime import date, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# 2026-os dátumok (ISO)
_SELECTIVE_2026 = {
    "2026-01-08", "2026-01-22", "2026-02-05", "2026-02-19", "2026-03-05", "2026-03-19",
    "2026-04-02", "2026-04-15", "2026-05-14", "2026-05-28", "2026-06-11", "2026-06-25",
    "2026-07-09", "2026-07-23", "2026-08-06", "2026-08-20", "2026-09-03", "2026-09-17",
    "2026-10-01", "2026-10-15", "2026-11-12", "2026-11-26", "2026-12-10", "2026-12-31",
}

_GREEN_2026 = {
    "2026-01-15", "2026-01-29", "2026-02-23", "2026-03-20", "2026-04-18",
    "2026-05-15", "2026-06-27", "2026-07-24", "2026-08-21", "2026-09-19",
}

def _parse_iso(d: str) -> date:
    y, m, dd = d.split("-")
    return date(int(y), int(m), int(dd))

def _next_from_dates(dates: set[date], today: date) -> date | None:
    future = sorted(d for d in dates if d >= today)
    return future[0] if future else None

def _next_weekly_tuesday_2026(today: date) -> date | None:
    """
    Kommunális (Vegyes): minden kedd 2026-ban
    (a forráskódod alapján: 2026-01-06 .. 2026-12-29).
    """
    start = date(2026, 1, 6)
    end = date(2026, 12, 29)

    if today <= start:
        return start
    if today > end:
        return None

    # Tuesday weekday index: 1 (Mon=0, Tue=1, ...)
    days_until = (1 - today.weekday()) % 7
    next_tuesday = today + timedelta(days=days_until)

    if next_tuesday < start:
        next_tuesday = start
    if next_tuesday > end:
        return None
    return next_tuesday

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            KajaszoKommunalisNextSensor(entry),
            KajaszoSzelektivNextSensor(entry),
            KajaszoZoldNextSensor(entry),
        ],
        update_before_add=True,
    )

class _BaseNextPickupSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, entry: ConfigEntry) -> None:
        self.entry = entry
        self._state: str | None = None
        self._attrs: dict = {}

    @property
    def native_value(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

    def _set_state(self, next_date: date | None, today: date):
        if next_date is None:
            self._state = None
            self._attrs = {
                "next_in_days": None,
                "note": "Nincs további dátum ebben az integrációban (csak 2026-ra van feltöltve).",
            }
            return

        self._state = next_date.isoformat()
        self._attrs = {
            "next_in_days": (next_date - today).days,
            "year": next_date.year,
        }

class KajaszoKommunalisNextSensor(_BaseNextPickupSensor):
    _attr_name = "Kajászó – Kommunális (következő)"
    _attr_unique_id = "kajaszo_waste_kommunalis_next"
    _attr_icon = "mdi:trash-can"

    async def async_update(self):
        today = date.today()
        next_date = _next_weekly_tuesday_2026(today)
        self._set_state(next_date, today)

class KajaszoSzelektivNextSensor(_BaseNextPickupSensor):
    _attr_name = "Kajászó – Szelektív (következő)"
    _attr_unique_id = "kajaszo_waste_szelektiv_next"
    _attr_icon = "mdi:recycle"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._dates = {_parse_iso(d) for d in _SELECTIVE_2026}

    async def async_update(self):
        today = date.today()
        next_date = _next_from_dates(self._dates, today)
        self._set_state(next_date, today)

class KajaszoZoldNextSensor(_BaseNextPickupSensor):
    _attr_name = "Kajászó – Zöld (következő)"
    _attr_unique_id = "kajaszo_waste_zold_next"
    _attr_icon = "mdi:leaf"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._dates = {_parse_iso(d) for d in _GREEN_2026}

    async def async_update(self):
        today = date.today()
        next_date = _next_from_dates(self._dates, today)
        self._set_state(next_date, today)
