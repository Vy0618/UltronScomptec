#pragma once
#include "telemetryModel.h"

void telemetryBegin();
void telemetryPublish(const MesaSnapshot& snapshot);
