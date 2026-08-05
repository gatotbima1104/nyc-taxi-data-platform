import json
from dataclasses import asdict

import apache_beam as beam
from apache_beam.io.gcp.pubsub import ReadFromPubSub
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from streaming.config import SUBSCRIPTION_PATH
from streaming.consumer.transformer import TaxiTransformer
from streaming.consumer.validator import EventValidator
from streaming.consumer.zone_lookup import TaxiZoneLookup


class PrintEvent(beam.DoFn):
    def __init__(self, title):
        self.title = title

    def process(self, event):
        print("=" * 60)
        print(self.title)
        print(
            json.dumps(
                event,
                indent=2,
                default=str,
            )
        )
        yield event

def run():
    options = PipelineOptions()
    standard_opt = options.view_as(StandardOptions)
    standard_opt.runner = "DirectRunner"
    standard_opt.streaming = True
    
    zone_lookup = TaxiZoneLookup()
    transformer = TaxiTransformer(zone_lookup)
    # validator = EventValidator()
    
    with beam.Pipeline(options=standard_opt) as pipeline:
        messages = (
            pipeline
            
            | "Read From PubSub"
            >> ReadFromPubSub(
                subscription=SUBSCRIPTION_PATH
            )
            
            | "Decode Json"
            >> beam.Map(
                lambda x: json.loads(
                    x.decode("utf-8")
                )
            )
        )
        
        transformed = (
            messages
            
            | "Transform Event"
            >> beam.Map(
                transformer.transform
            )
            
            | "Parsing to Dictionary"
            >> beam.Map(asdict)
        )
        
        (
            transformed
            
            | "Print Event"
            >> beam.ParDo(
                PrintEvent("Transformed Event")
            )
        )
        
        
        
        # validated = (
        #     messages
            
        #     | "Validate Event"
            
        #     >> beam.Map(
        #         validator.validate
        #     )
        # )
        
        # valid_event, invalid_event = (
        #     validated
            
        #     | "Events Partition"
        #     >> beam.Partition(
        #         validator.partition,
        #         2
        #     )
        # )
        
if __name__ == "__main__":
    run()