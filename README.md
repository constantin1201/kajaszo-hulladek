Kajászó Waste Schedule (2026) – Home Assistant Custom Integration

This is a custom Home Assistant integration that provides waste collection schedules for Kajászó (Hungary) for the year 2026.

The integration exposes three separate sensors, each always showing the next upcoming collection date:

🗑️ Kommunális (Vegyes)

♻️ Szelektív

🌿 Zöldhulladék

✨ Features

3 dedicated sensors (one per waste type)

Sensor state = next collection date (YYYY-MM-DD)

Attribute next_in_days = days until next pickup

UI-based setup (no YAML configuration required)

Lightweight, local calculation (no external API)

Based on official 2026 collection dates

🧩 Sensors Created
Sensor name	Description
Kajászó – Kommunális (következő)	Weekly pickup (every Tuesday in 2026)
Kajászó – Szelektív (következő)	Fixed date list
Kajászó – Zöld (következő)	Fixed date list

Each sensor exposes:

State: next pickup date (ISO format)

Attributes:

next_in_days

year

🚀 Installation
Manual installation

Copy the integration folder to your Home Assistant config directory:

config/custom_components/kajaszo_waste/


Restart Home Assistant

Go to:

Settings → Devices & Services → Add Integration


Search for:

Kajászó Waste Schedule (2026)


Add it — no configuration required 🎉

🔔 Notifications (optional)

The sensors are ideal for automations, for example:

Notify the evening before a pickup

Different notifications per waste type

Example condition:

{{ state_attr('sensor.kajaszo_kommunalis', 'next_in_days') == 1 }}

🛠 Technical Notes

Collection dates are hard-coded for 2026

After 2026 the sensors will return unknown

Designed to be easily extended for future years

📦 Source & Credits

Based on data structure inspired by:

https://github.com/mampfes/hacs_waste_collection_schedule

This integration is not affiliated with Home Assistant or the municipality.
