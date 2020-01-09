## happy path
* greet
    - utter_greet
* see_menu
    - find_menu
* inform{"menu": "lunch"} 
    - slot{"menu": "lunch"}
    - order_form_type
    - form{"name": "order_form_type"}
* inform_type{"item": "pizza", "quantity":"one"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform_type{"category":"margherita"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"size": "small"}  
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"quantity":"5"}
    - order_form_type
    - form{"name": "order_form_type"}
* choose{"confirmation":"False"}
    - order_form_type
    - form{"name": "order_form_type"}
    - form{"name": null}
* deny
    - action_deactivate_form
    - form{"name": null}
    - place_order


## happy path 12
* greet
    - utter_greet
* do_order
    - order_form_type
    - form{"name": "order_form_type"}
* inform_type{"item": "pizza", "category":"cheese n corn","quantity":"one"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"size": "small"}  
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"quantity":"5"}
    - order_form_type
    - form{"name": "order_form_type"}
* choose{"confirmation":"False"}
    - order_form_type
    - form{"name": "order_form_type"}
    - form{"name": null}
* deny
    - action_deactivate_form
    - form{"name": null}
    - place_order

## happy path 13
* greet
    - utter_greet
* do_order
    - order_form_type
* inform_type{"item":"burger"}
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"category": "burger pizza- classic veg"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"quantity":"10"}
    - order_form_type
    - form{"name": "order_form_type"}
* choose{"confirmation":"False"}
    - order_form_type
    - form{"name": "order_form_type"}
    - form{"name": null}
* deny
    - action_deactivate_form
    - form{"name": null}
    - place_order


## happy path 2
* greet
    - utter_greet
* see_menu
    - find_menu
* inform{"menu": "breakfast"} 
    - slot{"menu": "breakfast"}
    - order_form_type
    - form{"name": "order_form_type"}
* inform_type{"item": "desserts"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform_type{"category":"lava cake"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"quantity":"5"}
    - order_form_type
    - form{"name": "order_form_type"}
* choose{"confirmation":"False"}
    - order_form_type
    - form{"name": "order_form_type"}
    - form{"name": null}
* inform_type{"item": "burger"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"category": "burger pizza- classic non veg"} 
    - order_form_type
    - form{"name": "order_form_type"}
* inform{"quantity":"two"}
    - order_form_type
    - form{"name": "order_form_type"}
* choose{"confirmation":"False"}
    - order_form_type
    - form{"name": "order_form_type"}
    - form{"name": null}
* deny
    - action_deactivate_form  
    - form{"name": null}
    - place_order

## happy greet
* greet
    - utter_greet

## say no
* deny
    - action_deactivate_form
    - form{"name": null}
    - place_order

## say yes
* affirm
  - find_menu

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
