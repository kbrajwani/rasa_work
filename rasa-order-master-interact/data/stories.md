## happy path
  - utter_greet
* inform{"item": "pizza", "category":"preprony","quantity":"one"} 
  -slot{"item": "pizza"} 
  -slot{"category": "preprony"} 
  -slot{"quantity": "one"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null}
* inform{"item": "burger"} 
  -slot{"item": "burger"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null}

## happy path 1
  - utter_greet
* inform{"item": "Margherita"} 
  -slot{"item": "Margherita"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null}
* inform{"item": "BURGER PIZZA- CLASSIC VEG","quantity":"10"} 
  -slot{"item": "BURGER PIZZA- CLASSIC VEG"} 
  -slot{"quantity": "10"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null} 

## happy path 2
  - utter_greet
* inform{"item": "burger"} 
  -slot{"item": "burger"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null} 
    
## happy path 22
  - utter_greet
* inform{"item": "BURGER PIZZA- CLASSIC VEG"} 
  - order_form
    - form{"name": "order_form"}
    - form{"name": null} 

## happy path 3
* inform{"item": "Lava Cake"} 
  -slot{"item": "Lava Cake"}
  - order_form
    - form{"name": "order_form"}
    - form{"name": null} 

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
