#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

#define I2C_PORT i2c0
#define SDA_PIN 4
#define SCL_PIN 5

#define AS5600_ADDR 0x36
#define AS5600_ANGLE_HIGH 0x0E
#define AS5600_ANGLE_LOW  0x0F

uint16_t as5600_read_raw_angle() {
    uint8_t reg = AS5600_ANGLE_HIGH;
    uint8_t buf[2];

    int ret = i2c_write_blocking(I2C_PORT, AS5600_ADDR, &reg, 1, true);
    if (ret < 0) return 0xFFFF;

    ret = i2c_read_blocking(I2C_PORT, AS5600_ADDR, buf, 2, false);
    if (ret < 0) return 0xFFFF;

    uint16_t raw = ((uint16_t)buf[0] << 8) | buf[1];
    raw &= 0x0FFF;
    return raw;
}

int main() {
    stdio_init_all();
    sleep_ms(2000);

    i2c_init(I2C_PORT, 400 * 1000);
    gpio_set_function(SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(SDA_PIN);
    gpio_pull_up(SCL_PIN);

    printf("time_ms,raw,angle_deg\n");

    while (1) {
        uint16_t raw = as5600_read_raw_angle();

        if (raw != 0xFFFF) {
            float angle_deg = (raw * 360.0f) / 4096.0f;
            printf("%lu,%u,%.2f\n", to_ms_since_boot(get_absolute_time()), raw, angle_deg);
        }

        sleep_ms(20);   // ~50 Hz
    }

    return 0;
}
