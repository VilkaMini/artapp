# REST API for art prices on artprice.com
This repository is a fully functional REST API that can predict art prices given 10 features or show last 10 predictions made.
## Input requirements:
    Predicting:
        Your input should be (use POST method):
        1. A dictionary with these 8 values.
            1. type -> One of these: ['Original artwork', 'Multiple'].
            2. year -> For more accurate results pick years from range: [1990-2020].
            3. category -> One of these: ['Painting', 'Drawing-Watercolor', 
                                          'Print-Multiple', 'Photography', 
                                          'Sculpture-Volume'].
            4. medium -> ['Oil/canvas', 'Acrylic', 'Mixed media', 'Watercolour', 'Lithograph', 
                            'Mixed media/paper', 'Oil/panel', 'Oil', 'Etching', 'Silkscreen', 
                            'Bronze', 'Gelatin silver print', 'Indian ink', 'Ink', 'C print'].
            5. size_y -> Width of the artpiece in centimeters. Accurate range: [0, 999].
            6. size_x -> Height of the artpiece in centimeters. Accurate range: [0, 999].
            7. size_z -> Depth of the artpiece in centimeters. Accurate range: [0, 999].
            8. condition -> One of these: ['excellent', 'good condition', 'default', 'mediocre', 'used'].  

## Usage with python request library:
```python
# Create a dictionary with all the required values
data = {
        "type": "Original artwork",
        "year": 2005,
        "category": "Sculpture-Volume",
        "medium": "Mixed media",
        "size_y": 250,
        "size_x": 50,
        "size_z": 60,
        "condition": "mediocre"
       }

# Request POST request via '/price' path (data must be passed as json type)
response = requests.post("https://tc-capstone-artprice.herokuapp.com/price", json=data)

# Get prediction
response_text = json.loads(response.text)
response_text['predicted'][0]

# To get 10 latest results use GET method via '/history' path
response = requests.get("https://tc-capstone-artprice.herokuapp.com/history")
response_text = json.loads(response.text)

```

## Usage with Postman:
### Using POST method:
<a href="https://imgur.com/MUrZfZT"><img src="https://i.imgur.com/MUrZfZT.png" title="source: imgur.com" /></a>

### Using GET method:
<a href="https://imgur.com/LUemf1H"><img src="https://i.imgur.com/LUemf1H.png" title="source: imgur.com" /></a>

## Handling errors:
1. Error: CHECK IF INPUT IS FORMATED CORRECTLY -> Data proccesing function could not return a valid feature list, please ensure your input meets input [requirements](#Input-requirements).
2. Error: MODEL FAILED TO PREDICT THE PRICE -> Model did not succeed in predicting values, in such case contact me through [linkedIn](https://www.linkedin.com/in/viliusalaunis/).
3. Error: METHOD NOT ALLOWED -> Check the method you are using.

## License:

The MIT License (MIT). Please see the [license file](./LICENSE) for more information.