//
//  FunctionButtons.cpp
//  
//
//  Created by Aduen on 5/7/15.
//  Copyright (c) 2015 Aduen. All rights reserved.
//

#include "FunctionButtons.h"

FunctionButtons::FunctionButtons(){
    n_btns = 0;
}

void FunctionButtons::run(){
    for (uint8_t i = 0; i < n_btns; ++i) {
        // check buttons state changes
        bool curr_state = digitalRead(btns[i].btn_pin);
        uint32_t state_t = millis() - btns[i].state_change_t;
        
        // do blinking changes
        if(btns[i].led_blink_action == btns[i].bstate || btns[i].led_blink_action == btns[i].fstate)
        {
            if(btns[i].led_blink_freq < millis() - btns[i].led_blink_pt)
            {
                btns[i].led_blink_state = !btns[i].led_blink_state;
                btns[i].led_blink_pt = millis();
                digitalWrite(btns[i].led_pin, btns[i].led_blink_state);
            }
        }
        
        // check on longpress, previous state is equal to current state (pressing), current state is DOWN, time has passed threshold, state is not LONG PRESS already
        if(btns[i].pstate == curr_state && !curr_state && btns[i].long_press_t < state_t && btns[i].fstate != LONG_PRESS)
        {
            btns[i].fstate = FunctionButtons::LONG_PRESS;
            if(btns[i].f_call) btns[i].f_call(i, LONG_PRESS);
            digitalWrite(btns[i].led_pin, 1);
            //btns[i].state_change_t = millis();
        }

        // check on button and function changes
        if(curr_state != btns[i].pstate){
            btns[i].pstate = curr_state;
            btns[i].state_change_t = millis();
            btns[i].bstate = curr_state ? BUTTON_UP:BUTTON_DOWN;

            // ignore first button up after long press
            if (btns[i].fstate == FunctionButtons::LONG_PRESS && btns[i].bstate == BUTTON_UP) continue;

            // disable long press on button down
            if (btns[i].fstate == FunctionButtons::LONG_PRESS && btns[i].bstate == BUTTON_DOWN)
            {
                // set function state to on but dont execute callback, this ignores the first function change after long press
                // this exits the long press  cleanly with a function-off
                btns[i].fstate = FUNCTION_ON;
                continue;
            }


            if(btns[i].b_call) btns[i].b_call(i, btns[i].pstate ? BUTTON_UP:BUTTON_DOWN);

            if(btns[i].pstate == btns[i].func_on_up && bool(btns[i].f_call))
            {
                btns[i].fstate = btns[i].fstate == FUNCTION_ON ? FUNCTION_OFF : FUNCTION_ON;
                digitalWrite(btns[i].led_pin, btns[i].fstate == FUNCTION_ON);
                if(btns[i].f_call) btns[i].f_call(i, btns[i].fstate);
            }
        }
    }
}

bool FunctionButtons::func_state(uint8_t btnid){
    return btns[btnid].fstate;
}

void FunctionButtons::reset_fbutton(uint8_t btnid)
{
	btns[btnid].fstate = false;
	btns[btnid].pstate = digitalRead(btns[btnid].btn_pin);
	digitalWrite(btns[btnid].led_pin, LOW);
}

void FunctionButtons::set_fbutton_state(uint8_t btnid, bool fstate)
{
    btns[btnid].fstate = fstate;
	btns[btnid].pstate = digitalRead(btns[btnid].btn_pin);
	digitalWrite(btns[btnid].led_pin, fstate);
}

void FunctionButtons::set_blink_action(uint8_t btnid, uint8_t action_state, uint16_t blink_f)
{
    btns[btnid].led_blink_action = action_state;
    btns[btnid].led_blink_state = false;
    btns[btnid].led_blink_pt = millis();
    btns[btnid].led_blink_freq = blink_f;
}

uint8_t FunctionButtons::add_fbutton(uint8_t btn, uint8_t led, btncall_delegate cb_func = NULL, btncall_delegate cb_btn_state = NULL, uint32_t long_press_t = 0xFFFFFFFF, bool func_on_up = true){
    pinMode(btn, INPUT_DISABLE);
    pinMode(led, OUTPUT);
    digitalWrite(led, LOW);

    btns[n_btns].btn_pin = btn;

    // led states for blink or static
    btns[n_btns].led_pin = led;
    btns[n_btns].led_blink_state = false;
    btns[n_btns].led_blink_action = NULL;
    btns[n_btns].led_blink_pt = 0xFFFFFFFF;
    btns[n_btns].led_blink_freq = 0xFFFF;

    btns[n_btns].fstate = FunctionButtons::FUNCTION_OFF;
    btns[n_btns].pstate = digitalRead(btn);
    btns[n_btns].bstate = FunctionButtons::BUTTON_UP;
    
    // long press options
    btns[n_btns].state_change_t = millis();
    btns[n_btns].long_press_t = long_press_t;
    
    // call back functions
    btns[n_btns].f_call = cb_func;
    btns[n_btns].b_call = cb_btn_state;
    btns[n_btns].func_on_up = func_on_up;
    
    n_btns++;
    
    return n_btns-1;
}
