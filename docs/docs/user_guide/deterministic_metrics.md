# Deterministic metrics

ContextCheck implements following metrics:

* **Contains** - Checks if answer contains string

* **Case insensitive contains** - Case insensitive version of "contains"

* **Contains all** - Checks if answer contains all strings

* **Case insensitive contains all** - Case insensitive version of "contains all"

* **Contains any** - Check if answer contains at least one of the specified strings

* **Case insensitive contains any** - Case insensitive version of "contains any"

* **Is valid json** - Checks if the answer (in the string format) can be converted into a valid JSON

* **Has valid json schema** - Checks if the response is valid JSON and allows custom schema validations

* **Equals** - Checks if the answer matches 1-to-1 the expected answer

* **Regex** - Allows to use regular expressions to validate the format of the answer, match specific patterns, and ensure that the content adheres to a predefined structure.


All of the deterministic metrics validate AI-generated response. Refer to details and examples below.


## Contains and icontains

* **Description**: Checks if answer contains string

* **Name in YAML test scenarios**: `contains` and `icontains` for case insensitive version


Example:
```yaml
steps:
  - name: Example of contains and icontains
    request:
      message: "What is the capital of France?"
    asserts:
      - kind: contains
        assertion: "Paris"
      - kind: icontains
        assertion: "city"
```


## Contains all and icontains-all

* **Description**: Checks if answer contains all specified strings

* **Name in YAML test scenarios**: `contains-all` and `icontains-all` for case insensitive version


Example:
```yaml
steps:
  - name: Example of contains-all and icontains-all
    request:
      message: "List the primary colors."
    asserts:
      - kind: contains-all
        assertion: ["Red", "Blue", "Yellow"]
      - kind: icontains-all
        assertion: ["primary", "colors"]
```


## Contains any and icontains-any

* **Description**: Checks if answer contains at least one of the specified strings

* **Name in YAML test scenarios**: `contains-any` and `icontains-any` for case insensitive version


Example:
```yaml
steps:
  - name: Example of contains-any and icontains-any
    request:
      message: "Name a few famous scientists together with their matching fundamental branch of science"
    asserts:
      - kind: contains-any
        assertion: ["Einstein", "Newton", "Darwin"]
      - kind: icontains-any
        assertion: ["theory of relativity", "laws of motion", "theory of evolution"]
```


## Is valid json

* **Description**: Checks if the answer (returned by default in string format) can be converted into a valid JSON

* **Name in YAML test scenarios**: `is-valid-json`


Example:
```yaml
steps:
  - name: Example of is-valid-json
    request:
      message: "Give me a JSON object representing a person."
    asserts:
      - kind: is-valid-json
```


## Has valid json schema

* **Description**: Checks if the JSON response adheres to a specified JSON schema. It can check for presence of specific fields, validate data types, enforce required properties, and apply 
constraints such as string length or numerical ranges.
* **Name in YAML test scenarios**: `has-valid-json-schema`


Example below shows an hypothetical system where given user query "I'm looking for t-shirt size L, blue color and small drawing of cat" the system is expected to return a list of JSON formatted products in format:
```json
{
  "products": [
    {
		"name": "Blue Cat Print T-Shirt",
		"size": "L",
		"color": "Blue",
		"price": 29.99,
		"inStock": true,
		"features": ["100% Cotton", "Cat Design", "Machine Washable"],
		"description": "A comfortable blue t-shirt with a small, adorable cat design. Perfect for cat lovers!"
	},
	[ ... more products ... ]
	],
	"totalResults": 4
}
```

Matching `has-valid-json-schema` definition would look as follows:

```yaml
steps:
  - name: Sophisticated example of has-valid-json-schema
    request:
      message: "I'm looking for t-shirt size L, blue color and small drawing of cat"
    asserts:
      - kind: has-valid-json-schema
        assertion:
          type: object
          properties:
            products:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    minLength: 5
                    maxLength: 100
                  size:
                    type: string
                    enum: ["S", "M", "L", "XL", "XXL"]
                  color:
                    type: string
                  price:
                    type: number
                    minimum: 0
                    exclusiveMaximum: 100
                  inStock:
                    type: boolean
                  features:
                    type: array
                    items:
                      type: string
                  description:
                    type: string
                    maxLength: 500
                required: ["name", "size", "color", "price", "inStock"]
            totalResults:
              type: integer
              minimum: 5
          required: ["products", "totalResults"]
```

If you're new to JSON Schema, the [Miscellaneous Examples](https://json-schema.org/learn/miscellaneous-examples) from the JSON Schema Community 
are helpful for getting started and understanding its capabilities. For more in-depth information, we recommend the [JSON Schema Reference](https://json-schema.org/understanding-json-schema/reference).


## Equals

* **Description**: Checks if the answer matches 1-to-1 the expected answer
* **Name in YAML test scenarios**: `equals`

Example:
```yaml
steps:
  - name: Example of equals
    request:
      message: "What is 2 + 2?"
    asserts:
      - kind: equals
        assertion: "4"
```


## Regex

* **Description**: Allows use of regular expressions to validate the format of the answer
* **Name in YAML test scenarios**: `regex`

Example:
```yaml
steps:
  - name: Example of regex
    request:
      message: "What is the email address of the HR department?"
    asserts:
      - kind: regex
        assertion: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
```
