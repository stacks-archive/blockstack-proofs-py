# proofchecker
For verifying proofs (twitter, github, domains etc) linked to a blockchain ID

# Usage 

First install the package:

> pip install proofchecker

Then:
```
from proofchecker import profile_to_proofs
proofs = profile_to_proofs(username, profile)
```

The username above refers to the blockchain ID username and profile is the json profile of the respective blockchain ID.
