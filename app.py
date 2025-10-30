from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

home_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Blood Request Service</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        h1 { color: darkgreen; }
        input, select, button { padding: 8px; margin: 5px 0; }
        button { background: #28A745; color: white; border: none; border-radius: 5px; cursor: pointer; }
        ul { list-style-type: none; padding: 0; }
        li { padding: 5px; background: #f0f0f0; margin-bottom: 5px; border-radius: 5px; }
        a.button { display: inline-block; padding: 8px 15px; background: #007BFF; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Blood Request Service</h1>
    <a class="button" href='http://localhost:5001/donors'>Go to Donor Service</a>
    
    <h2>Search Donors:</h2>
    Blood Group: 
    <select id="blood_group">
        <option>A+</option><option>A-</option><option>B+</option><option>B-</option>
        <option>O+</option><option>O-</option><option>AB+</option><option>AB-</option>
    </select><br>
    City: <input id="city" placeholder="Enter city"><br>
    <button onclick="requestBlood()">Request Blood</button>

    <h2>Results:</h2>
    <ul id="result"></ul>

<script>
function requestBlood() {
    let blood_group = document.getElementById('blood_group').value;
    let city = document.getElementById('city').value;

    fetch('/request_blood', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({blood_group, city})
    })
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById('result');
        list.innerHTML = '';
        if(data.donors.length === 0){
            list.innerHTML = '<li>No donors found</li>';
        } else{
            data.donors.forEach(d => {
                let li = document.createElement('li');
                li.textContent = d.name + ' - ' + d.blood_group + ' - ' + d.city;
                list.appendChild(li);
            });
        }
        alert(data.message);
    });
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_page)

@app.route('/request_blood', methods=['POST'])
def request_blood():
    data = request.json
    # Donor service API call
    try:
        response = requests.get('http://donor_service:5001/all_donors')
        donors = response.json()
    except:
        return jsonify({"message": "Cannot reach Donor Service!", "donors": []})
    
    matched = [d for d in donors if d['blood_group'].lower() == data['blood_group'].lower() and d['city'].lower() == data['city'].lower()]
    return jsonify({"message": f"Found {len(matched)} donor(s).", "donors": matched})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)