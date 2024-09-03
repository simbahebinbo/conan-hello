#!/bin/bash

conan remove hello/1.0.0 -c
conan create . --build=missing --update