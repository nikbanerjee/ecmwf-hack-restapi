#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()
server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "2006-01-01/to/2016-12-31",
    "expver": "1",
    "grid": "0.75/0.75",
    "levtype": "sfc",
    "param": "34.128/141.128/164.128/167.128/189.128/228.128",
    "step": "3",
    "stream": "oper",
    "time": "12:00:00",
    "type": "fc",
    "target": "yearly_data.grib",
})
