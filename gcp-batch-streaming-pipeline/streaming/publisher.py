import json
import time

import pandas as pd
from google.cloud import pubsub_v1

from schema import build_event
from constants.constant import (
    EVENTS_PER_SECOND,
    PARQUET_PATH,
    PROJECT_ID,
    TOPIC_ID,
)

publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(
    PROJECT_ID,
    TOPIC_ID,
)


def publish(max_events: int = 5):
    df = pd.read_parquet(PARQUET_PATH)

    interval = 1 / EVENTS_PER_SECOND

    try:
        for index, row in df.head(max_events).iterrows():

            event = build_event(row.to_dict())

            payload = json.dumps(
                event,
                default=str
            ).encode("utf-8")

            future = publisher.publish(
                topic_path,
                payload
            )

            message_id = future.result()

            print(
                f"[{index + 1}/{max_events}] "
                f"Published "
                f"message_id={message_id} "
                f"pickup={event['lpep_pickup_datetime']} "
                f"total_amount={event['total_amount']}"
            )

            time.sleep(interval)

        print("\nSuccessfully published all test events.")

    except KeyboardInterrupt:
        print("\nPublisher stopped safely.")

    except Exception as e:
        print(f"\nError publishing message: {e}")


if __name__ == "__main__":
    publish()