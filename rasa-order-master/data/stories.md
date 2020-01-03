## happy path
* greet
  - find_menu
* inform{"menu": "lunch"} 
  -slot{"menu": "lunch"} 
  - find_sub_menu
* inform{"menu": "pizza"} 
  -slot{"menu": "pizza"} 
  - find_sub_menu
* inform{"menu": "Margherita"} 
  -slot{"menu": "Margherita"} 
  - find_sub_menu
* inform{"item": "small"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null} 
* affirm
  - utter_affirm

## happy path 2
* greet
  - find_menu
* inform{"menu": "lunch"} 
  -slot{"menu": "lunch"} 
  - find_sub_menu
* inform{"menu": "burger"} 
  -slot{"menu": "burger"} 
  - find_sub_menu
* inform{"item": "BURGER PIZZA- CLASSIC VEG"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null}
* affirm
  - utter_affirm

## happy path 3
* inform{"item": "Lava Cake"} 
  -slot{"item": "Lava Cake"}
  - order_form
    - form{"name": "order_form"}
    - form{"name": null}
* affirm
  - utter_affirm

## say no
* deny
  - find_menu

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
