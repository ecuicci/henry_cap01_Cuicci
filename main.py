from flask import Flask, request, jsonify

app = Flask(__name__)

def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers

def filter_even(numbers):
    return [num for num in numbers if num % 2 == 0]

def sum_elements(numbers):
    return sum(numbers)

@app.route('/bubble-sort', methods=['POST'])
def bubble_sort_endpoint():
    data = request.get_json()
    numbers = data.get('numbers', [])
    sorted_numbers = bubble_sort(numbers)
    return jsonify({"numbers": sorted_numbers})

@app.route('/filter-even', methods=['POST'])
def filter_even_endpoint():
    data = request.get_json()
    numbers = data.get('numbers', [])
    even_numbers = filter_even(numbers)
    return jsonify({"even_numbers": even_numbers})

@app.route('/sum-elements', methods=['POST'])
def sum_elements_endpoint():
    data = request.get_json()
    numbers = data.get('numbers', [])
    total_sum = sum_elements(numbers)
    return jsonify({"sum": total_sum})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)