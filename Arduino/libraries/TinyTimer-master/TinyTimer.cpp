#include "TinyTimer.h"

TinyTimer::TinyTimer() {
    uint16_t currentMillis = millis();

    for (int i = 0; i < MAX_TIMERS; i++) {
        calls[i].enabled = false;
        calls[i].callback = 0;
        calls[i].prevMillis = currentMillis;
        calls[i].params = -1;
    }

    numTimers = 0;
}


void TinyTimer::run() {
    // get current time
    uint32_t currentMillis = millis();

    for (uint8_t i = 0; i < MAX_TIMERS; i++) {

        // only process active timers
        if (!calls[i].callback || !calls[i].enabled) continue;

		// is it time to process this timer ?
		if (currentMillis - calls[i].prevMillis >= calls[i].delay) {

			// update time
			calls[i].prevMillis = currentMillis;

			// "run forever" timers must always be executed
			if (calls[i].maxRuns == RUN_FOREVER) {
				(calls[i].callback)(calls[i].params);
			}
			// other timers get executed the specified number of times

			else if (calls[i].numRuns < calls[i].maxRuns) {
				(calls[i].callback)(calls[i].params);
				calls[i].numRuns++;

				// after the last run, delete the timer
				// to save some cycles
				if (calls[i].numRuns >= calls[i].maxRuns) {
					deleteTimer(i);
				}
			}
        }
    }
}

uint8_t TinyTimer::setTimer(long d, void(*f_ptr)(uint8_t), uint8_t n) {
	if (numTimers >= MAX_TIMERS) {
        return -1;
    }

    uint8_t free_spot = getAvailableSpot();
    if(free_spot < 0)return -1;

    calls[free_spot].delay = d;
    calls[free_spot].callback = f_ptr;
    calls[free_spot].maxRuns = n;
    calls[free_spot].enabled = true;
    calls[free_spot].numRuns = 0;
    calls[free_spot].prevMillis = millis();
    calls[free_spot].params = free_spot;

    numTimers = getNumTimers();

    return free_spot;
}

uint8_t TinyTimer::setTimer(long d, void(*f_ptr)(uint8_t), uint8_t n, uint8_t param) {
    if (numTimers >= MAX_TIMERS) {
        return -1;
    }

    uint8_t free_spot = getAvailableSpot();
    if(free_spot < 0)return -1;

    calls[free_spot].delay = d;
    calls[free_spot].callback = f_ptr;
    calls[free_spot].maxRuns = n;
    calls[free_spot].enabled = true;
    calls[free_spot].numRuns = 0;
    calls[free_spot].prevMillis = millis();
    calls[free_spot].params = param;

    numTimers = getNumTimers();

    return free_spot;
}

uint8_t TinyTimer::setInterval(long d, void(*f_ptr)(uint8_t)) {
    return setTimer(d, f_ptr, RUN_FOREVER);
}


uint8_t TinyTimer::setTimeout(long d, void(*f_ptr)(uint8_t)) {
    return setTimer(d, f_ptr, RUN_ONCE);
}

void TinyTimer::changeDelay(uint8_t numTimer, uint16_t d){
	calls[numTimer].delay = d;
	calls[numTimer].prevMillis = millis();
}

void TinyTimer::deleteTimer(uint8_t numTimer) {
    if (numTimer >= MAX_TIMERS) {
        return;
    }

    // nothing to disable if no timers are in use
    if (numTimers == 0) {
        return;
    }

    calls[numTimer].callback = 0;
    calls[numTimer].enabled = false;
    calls[numTimer].delay = 0;

    numTimers = getNumTimers();
}


boolean TinyTimer::isEnabled(uint8_t numTimer) {
    if (numTimer >= MAX_TIMERS) {
        return false;
    }

    return calls[numTimer].enabled;
}


void TinyTimer::enable(uint8_t numTimer) {
    if (numTimer >= MAX_TIMERS) {
        return;
    }

    calls[numTimer].enabled = true;
}


void TinyTimer::disable(uint8_t numTimer) {
    if (numTimer >= MAX_TIMERS) {
        return;
    }

    calls[numTimer].enabled = false;
}


void TinyTimer::toggle(uint8_t numTimer) {
    if (numTimer >= MAX_TIMERS) {
        return;
    }

    calls[numTimer].enabled = !calls[numTimer].enabled;
}

int8_t TinyTimer::getAvailableSpot() {
	for (int i = 0; i < MAX_TIMERS; i++) {
		if(calls[i].callback == 0)return i;
	}
	return -1;
}

uint8_t TinyTimer::getNumTimers() {
	uint8_t numTimers = 0;
    for (int i = 0; i < MAX_TIMERS; i++) {
		if(calls[i].callback && calls[i].enabled)numTimers++;
	}
    return numTimers;
}
