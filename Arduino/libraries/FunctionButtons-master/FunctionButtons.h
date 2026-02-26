//
//  FunctionButtons.h
//  
//
//  Created by Aduen on 5/7/15.
//  Copyright (c) 2015 Aduen. All rights reserved.
//

#ifndef FunctionButtons_h
#define FunctionButtons_h

#include <Arduino.h>

typedef void (*btncall_delegate)(uint8_t, uint8_t);

typedef struct {
    uint8_t btn_pin;
    uint8_t led_pin;
    uint16_t led_blink_freq;
    uint32_t led_blink_pt;
    uint8_t led_blink_action;
    bool led_blink_state;

    bool pstate;
    uint8_t fstate;
    uint8_t bstate;
    uint32_t state_change_t;
    uint32_t long_press_t;

    bool func_on_up;
    btncall_delegate f_call;
    btncall_delegate b_call;

} btn_struct;

class FunctionButtons {
public:
    const uint8_t static BUTTON_UP = 1;
    const uint8_t static BUTTON_DOWN = 2;
    const uint8_t static LONG_PRESS = 20;
    const uint8_t static FUNCTION_ON = 3;
    const uint8_t static FUNCTION_OFF = 4;
    
    FunctionButtons();
    
    uint8_t add_fbutton(uint8_t btn, uint8_t led, btncall_delegate cb_func = NULL, btncall_delegate cb_btn_state = NULL, uint32_t long_press_t = 0xFFFFFFFF, bool func_on_up = true);
	void set_blink_action(uint8_t btnid, uint8_t state, uint16_t blink_freq);
    void reset_fbutton(uint8_t btnid);
    void set_fbutton_state(uint8_t btnid, bool fstate);
    
    bool func_state(uint8_t btnid);
    void run();
    
private:
    btn_struct btns[3];
    uint8_t n_btns;
    
};

#endif
