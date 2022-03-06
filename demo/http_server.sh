#!/bin/bash

echo \"Hello, World -- from 2a!\" > index.html
nohup sudo python3 -m http.server 80 &