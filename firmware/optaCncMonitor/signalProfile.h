#pragma once
#include <stddef.h>
#include <stdint.h>

namespace ultron {
constexpr size_t DIGITAL_SIGNAL_COUNT = 6;
constexpr uint8_t DIGITAL_INPUT_MASK = 0x3F;
constexpr const char* DIGITAL_SIGNAL_NAMES[DIGITAL_SIGNAL_COUNT] = {
    "ativo", "inativo", "emergencia", "motor_ligado", "alarme", "porta_aberta"};
constexpr uint8_t SPARE_INPUT_NUMBER = 7;
constexpr uint8_t CURRENT_INPUT_NUMBER = 8;
// I8/A7 is reserved. No ADC read or conversion is valid without a sensor/calibration.
constexpr bool CURRENT_PHYSICAL_ENABLED = false;
constexpr const char* SIGNAL_PROFILE = "six_signals_current_reserved_v2";
}
