class Helper:
    
    @staticmethod
    def producer_log(
        TOPIC_ID,
        EVENTS_PER_INTERVAL,
        PUBLISH_INTERVAL_SECONDS,
        dry_run
    ):
        print("=" * 60)
        print("Taxi Event Publisher Started")
        print(f"Topic            : {TOPIC_ID}")
        print(f"Events/Interval  : {EVENTS_PER_INTERVAL}")
        print(f"Interval         : {PUBLISH_INTERVAL_SECONDS} second(s)")
        print(f"Dry Run          : {dry_run}")
        print("=" * 60)
        
    @staticmethod
    def consumer_log(event: dict, status: str):
        message = f"{status:<11} event_id={event['event_id']}"
        
        if status == "QUARANTINE":
            message += f' issue="{event["issue_description"]}"'

        print(message)
        return event