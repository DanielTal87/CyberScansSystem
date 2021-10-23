# Cyber Scans System

## Description

System for dispatching cyber scans

## Requirements

1. Python 3.9.X
2. Redis server

## How to run

1. In the project directory, run: `./install.sh`
2. In new terminal tab, run `redis-server`
3. In new terminal tab, run `rq worker`
4. In terminal run `./run.sh`
5. Check today's logs at: `/logs`

## Routes

1. Health Check - ```GET http://127.0.0.1:5000/health-check```
2. Ingest - ```POST http://127.0.0.1:5000/ingest```
3. Status - ```GET http://127.0.0.1:5000/status/<scan_id:string>```

## Background Process

Every 30 seconds the server update all the scans states

* the interval can be configured in the config.json file

## Examples

API examples for CURL (run in terminal)

1. Health Check - ```curl 'http://127.0.0.1:5000/health-check'```
2. Ingest - ```curl -X POST 'http://127.0.0.1:5000/ingest'```
3. Status - ``` curl 'http://127.0.0.1:5000/status/<scan_id:string>'``` 

