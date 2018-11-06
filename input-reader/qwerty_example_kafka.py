from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka import admin
import IPython
import time
import sys

config = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'mygroup',
    'enable.auto.commit': False
}
administrator = admin.AdminClient(config)

result = administrator.create_topics([admin.NewTopic("mytopic5", 2, 1)], validate_only=True)

p = Producer(config)

start_input = time.time()
for data in range(20, 30):
    data = str(data)
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    IPython.embed()
    p.produce('mytopic4', data.encode('utf-8')) #, callback=delivery_report)
print("UP", time.time() - start_input)
    
# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()

c = Consumer(config)

c.subscribe(['mytopic4'])

value = ''
prev_value = ''
values_seen = []
start_time = time.time()
while True:
    msg = c.poll(1/sys.float_info.max)

    if msg is None:
        continue
    IPython.embed()
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break
    value = msg.value()
    if value not in values_seen:
        print(value)
        values_seen.append(value)
    if len(values_seen) == 10:
        break
        
print("Down", time.time() - start_time)
c.close()
