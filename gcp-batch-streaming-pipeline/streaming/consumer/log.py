import json

import apache_beam as beam


class LogEvent(beam.DoFn):
    def __init__(self, event_type: str):
        self.event_type = event_type.upper()

    def process(self, event):
        if self.event_type == "RAW":
            payload = {
                "event_id": event.get("event_id"),
                "event_time": event.get("event_time"),
                "publish_time": event.get("publish_time"),
            }

        elif self.event_type == "CURATED":
            payload = {
                "event_id": event.get("event_id"),
                "event_time": event.get("event_time"),
                "publish_time": event.get("publish_time"),
                "ingestion_time": event.get("ingestion_time"),
            }

        elif self.event_type == "QUARANTINE":
            payload = {
                "event_id": event.get("event_id"),
                "event_time": event.get("event_time"),
                "publish_time": event.get("publish_time"),
                "ingestion_time": event.get("ingestion_time"),
                "issue_description": event.get("issue_description"),
            }

        else:
            payload = event

        print("=" * 60)
        print(self.event_type)
        print(
            json.dumps(
                payload,
                indent=2,
                default=str,
            )
        )

        yield event