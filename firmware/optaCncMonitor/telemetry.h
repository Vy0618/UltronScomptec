#pragma once
#include "telemetryModel.h"

void telemetryBegin();
void telemetryPublish(const CncSnapshot& snapshot);
