from flask import Flask, request, jsonify, render_template, url_for, session, redirect
from pymongo import MongoClient
from keygen import generate_keys
import BCMaker as bc


app = Flask(__name__)


app.secret_key = 'safsabfuhfqoieh243eq'
## Sample data
voter = {"name": "voter 1", "id": "1020302010", "phone":"10203010203", "age":"40"}  # Sample voter data
options = [{"name": "Option 1"}, {"name": "Option 2"}, {"name": "Option 3"}]  # Sample options
# List to store the votes
 # Sample vote record

# BC maker ki config
blockchain_data = [bc.genesisGen()]
voting_started = False
verification_key = "uid" # yahan apni key daalni hai yaad se

# MongoDB ki configuration
client = MongoClient('dbCode')
db = client['votemaxxing']
collection = db['db1']
voteCheckDB = db['db2']
candiListDB = db['candList']

@app.route('/')
def home():
    return render_template('signin.html')


@app.route('/homeDash')
def homeDash():
    user = session.get('user')  # Get the current user's information
    if not user:  # If no user is signed in
        return redirect(url_for('home'))  # Redirect to the sign in page
    return render_template('dash.html', user=user)  # Pass the user's information to the template

@app.route('/voteDash') #dashboard
def vote():
    return render_template('voter.html', voter=session['user'])

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/cast_vote', methods=['GET']) # Voting Page
def cast_vote():
    return render_template('cast-vote.html', user=session['user'], options=options)

@app.route('/submit_vote') #thank you 
def submit_vote():
    selected_option = request.args.get('selected_option')
    print(selected_option+" selected by voter "+ voter["name"])
    # Store the selected option in a variable
    # You can now use the selected_option variable in your code
    return render_template('thank_you.html')

@app.route('/register')
def register():
    return render_template('registration.html')


@app.route('/SignUsr', methods=['POST'])
def sign_in():
    data = request.json
    # User existence checking
    user = collection.find_one({'uid': data['uid'], 'password': data['password']})
    if user:
        # Save the user's data in the session
        session['user'] = {
            'uid': user['uid'],
            'name': user['name'],
            'age': user['age'],
            'phone': user['phone'],
            'Public': user['public_key']
            # Add other user attributes as needed
        }
        # Return a JSON response with a redirect_url field
        return jsonify({"success": True, "redirect_url": url_for('homeDash')})
    else:
        return jsonify({"success": False, "message": "Sign In failed. Invalid credentials"})

@app.route('/regUsr', methods=['POST'])
def register_user():
    data = request.json
    # duplicate cheking
    existing_user = collection.find_one({'uid': data['uid']})
    if existing_user:
        return jsonify({"success": False, "message": "User already exists with this UID"})
    else:
        # put data in mongo
        dataFin = generate_keys(data)
        collection.insert_one(dataFin)
        return jsonify({"success": True, "message": "User registration successful"})

@app.route('/startVoting', methods=['POST'])
def startVote():
    global voting_started
    #key = request.form.get('key') Yaad se isk bhi krna hai 
    key = "uid"
    if key == verification_key:
        voting_started = True
        return jsonify({"message": "Voting started!"}), 200
    else:
        return jsonify({"error": "Invalid verification key"}), 401

@app.route('/isStarted')
def is_started():
    global voting_started
    return jsonify(voting_started) 

@app.route('/hasVoted', methods=['POST'])
def has_voted():
    uid = request.json.get('uid')
    if not uid:
        return {"error": "No UID provided"}, 400

    # Check if the UID exists in voteCheckDB
    existing_vote = voteCheckDB.find_one({"UID": uid})

    # If it exists, delete it
    if existing_vote:
        voteCheckDB.delete_one({"UID": uid})

    # Insert a new document with the UID and flag set to true
    voteCheckDB.insert_one({"UID": uid, "flag": True})

    return {"message": "Vote recorded"}, 200

@app.route('/dupeCheck')
def dupe_check():
    user = session.get('user')
    print(user)
    uid = user['uid'] if user else None  # changed user.uid to user['uid']
    print(uid)
    if uid is None:
        return jsonify(False)  # return false if no user is in session

    user_vote = voteCheckDB.find_one({'uid': uid})
    if user_vote is not None and user_vote.get('flag', False):
        print("true")
        return jsonify(True)  # return true if user has voted (flag is true)

    print("false")
    return jsonify(False)  # return false if user has not voted or doesn't exist

@app.route('/candiList')
def candi_list():
    candidates = candiListDB.find()  # get all documents
    candidate_list = [{'CID': candidate['CID'], 'name': candidate['name']} for candidate in candidates]  # extract the CID and names
    return jsonify(candidate_list)  # return the list as a JSON array


@app.route('/candiUpdate', methods=['POST'])
def candi_update():
    candidates = request.get_json()  # get the list of candidates from the request body
    if not candidates:
        return jsonify({'error': 'No data provided'}), 400  # return an error if no data is provided

    # Delete all existing documents in the collection
    candiListDB.delete_many({})

    # Insert the new candidates into the collection
    candiListDB.insert_many(candidates)

    return jsonify({'message': 'Candidates updated successfully'}), 200  # return a success message



@app.route('/recieveVotes', methods=['POST']) # ye form-data lega, JSON nhi lega dont even try nigga
def recVotes():
    global voting_started, blockchain_data
    if not voting_started:
        return jsonify({"error": "Voting has not started yet"}), 400

    encrypted_object = request.form.get('encrypted_object')
    bc.addBlck(blockchain_data, encrypted_object)
    return jsonify({"message": "Vote received and added to the blockchain"}), 200

@app.route('/endVote', methods=['POST'])
def endVote():
    global voting_started, blockchain_data
    if not voting_started:
        return jsonify({"error": "Voting has not started yet"}), 400

    bc.svBChain(blockchain_data)
    voting_started = False
    return jsonify({"message": "Voting ended. Blockchain saved."}), 200

@app.route('/manage_voters', methods=['POST'])
def manage_voters():
    return 0
#     voters = mongo.db.voters
#     voter_id = request.form.get('voter_id')
#     voter_name = request.form.get('voter_name')
#     voter_phone = request.form.get('voter_phone')
#     voter_age = request.form.get('voter_age')
#     action = request.form.get('action')

#     if action == 'Add Voter':
#         voters.insert_one({'_id': voter_id, 'name': voter_name, 'phone': voter_phone, 'age': voter_age})
#     elif action == 'Update Voter':
#         voters.update_one({'_id': voter_id}, {'$set': {'name': voter_name, 'phone': voter_phone, 'age': voter_age}})
#     elif action == 'Delete Voter':
#         voters.delete_one({'_id': voter_id})

#     return render_template('admin.html')

@app.route('/manage_candidates', methods=['POST'])
def manage_candidates():
    return 0
#     candidates = mongo.db.candidates
#     candidate_id = request.form.get('candidate_id')
#     candidate_name = request.form.get('candidate_name')
#     action = request.form.get('action')

#     if action == 'Add Candidate':
#         candidates.insert_one({'_id': candidate_id, 'name': candidate_name})
#     elif action == 'Update Candidate':
#         candidates.update_one({'_i6d': candidate_id}, {'$set': {'name': candidate_name}})
#     elif action == 'Delete Candidate':
#         candidates.delete_one({'_id': candidate_id})

@app.route('/results')
def results():
    return 0
    # results = mongo.db.results.find()
    # return render_template('results.html'

if __name__ == '__main__':
    app.run(debug=True)
