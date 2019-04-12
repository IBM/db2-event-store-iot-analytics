#!/usr/bin/python

import time
import numpy as np
import pandas as pd
import sys
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="generates 1000000 rows of sample records, or a given count of record if -c flag is specified")
    parser.add_argument("-c","--count", help="count of records to be generated",type=int)
    args = parser.parse_args()

    if args.count: 
        total_record = args.count
    else:
        total_record = 1000000

    np.random.seed(0)
    time_now = 1541019341*1000
    record_processed = 0
    df = [ ]

    while record_processed < total_record:
        deviceID = np.random.randint(1, 3)
        sensorID = np.random.randint(1, 50)
        env_temp = np.random.normal(24.5, 2)  # ambient temp 
        time_now += np.random.randint(10,1500)
        power = np.random.normal(10, 3) # power consumption
        noise = np.random.normal(0,1.5)
        temp = 1.3 * env_temp + 0.5 * power + 5 + noise

        df.append(dict(device=int(deviceID), sensor=int(sensorID), ts=time_now, env_temp=float(env_temp), power=float(power), temperature=float(temp)))
        record_processed += 1

    df = pd.DataFrame(df)
    df = df[['device', 'sensor', 'ts', 'env_temp', 'power', 'temperature']]
    df.to_csv("sample_IOT_table.csv", index=False, header=False)
    print("Maximum timestamp recorded is : {}".format( df['ts'].max() ))
    print("Minimum timestamp recorded is : {}\n".format( df['ts'].min() ))



