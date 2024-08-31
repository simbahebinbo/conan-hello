#!/bin/bash

conan remove hello/1.0.0 -c
conan create . --version=1.0.0 --name=hello --build=missing --update