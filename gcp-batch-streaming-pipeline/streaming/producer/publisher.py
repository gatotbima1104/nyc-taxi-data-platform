import json
import time

from constants.constant import PROJECT_ID, TOPIC_ID
from google.cloud import pubsub_v1
from streaming.config import EVENTS_PER_INTERVAL, PARQUET_FILE, PUBLISH_INTERVAL_SECONDS
from streaming.producer import BatchStatistics, TaxiEventGenerator

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
stats = BatchStatistics(PARQUET_FILE).load()
generator = TaxiEventGenerator(stats)


def publish(
    max_events: int | None = None,
    dry_run: bool = True,
):
    published = 0

    print("=" * 60)
    print("Taxi Event Publisher Started")
    print(f"Topic            : {TOPIC_ID}")
    print(f"Events/Interval  : {EVENTS_PER_INTERVAL}")
    print(f"Interval         : {PUBLISH_INTERVAL_SECONDS} second(s)")
    print(f"Dry Run          : {dry_run}")
    print("=" * 60)

    try:
        while max_events is None or published < max_events:
            
            for _ in range(EVENTS_PER_INTERVAL):
                if max_events is not None and published >= max_events:
                    break
                
                event = generator.generate()
                if dry_run:
                    print(json.dumps(event, indent=2, default=str))
                    
                else:
                    payload = json.dumps(event, default=str).encode("utf-8")
                    future = publisher.publish(topic_path, payload)
                    message_id = future.result()
                    
                    print(
                        f"[{published + 1}] "
                        f"Published "
                        f"message_id={message_id}"
                    )

                published += 1

            if max_events is None or published < max_events:
                time.sleep(PUBLISH_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nPublisher stopped safely.")

    except Exception as e:
        print(f"\nPublisher failed: {e}")

    finally:
        print(f"\nProcessed {published} event(s).")


if __name__ == "__main__":

    # Example:
    # 1 event every 5 seconds
    publish(max_events=2, dry_run=False)

    # Publish forever
    # publish(dry_run=False)