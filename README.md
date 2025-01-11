# Blockchain-Based-voting-platform

Blockchain is a technology that is rapidly gaining momentum in the era of industry 4.0. With high security and transparency provisions, it is being widely used in supply chain management systems, healthcare, payments, business, IoT, voting systems, etc.

## Why do we need it?

Current voting systems like ballot box voting or electronic voting suffer from various security threats such as DDoS attacks, polling booth capturing, vote alteration and manipulation, malware attacks, etc, and also require huge amounts of paperwork, human resources, and time. This creates a sense of distrust among existing systems.

Some of the disadvantages are:
- Long Queues during elections
- Security Breaches like data leaks, vote tampering.
- Lot of paperwork involved, hence less eco-friendly and time-consuming.
- Difficult for differently-abled voters to reach polling booth.
- Cost of expenditure on elections is high.

## Solution

Using blockchain, the voting process can be made more secure, transparent, immutable, and reliable. How? Let’s take an example.

Suppose you are an eligible voter who goes to a polling booth and casts a vote using EVM (Electronic Voting Machine). But since it’s a circuitry after all and if someone tampers with the microchip, you may never know that did your vote reach the person for whom you voted or was diverted into another candidate’s account? Since there’s no tracing back of your vote. But, if you use blockchain- it stores everything as a transaction that will be explained soon below; and hence gives you a receipt of your vote (in the form of a transaction ID) and you can use it to ensure that your vote has been counted securely.

Now suppose a digital voting system (website/app) has been launched to digitize the process and all confidential data is stored on a single admin server/machine, if someone tries to hack it or snoop over it, he/she can change the candidate’s vote count- from 2 to 22! You may never know that hacker installs malware or performs clickjacking attacks to steal or negate your vote or simply attacks the central server.

To avoid this, if the system is integrated with blockchain- a special property called immutability protects the system. Consider SQL, PHP, or any other traditional database systems. You can insert, update, or delete votes. But in a blockchain, you can just insert data but cannot update or delete. Hence when you insert something, it stays there forever and no one can manipulate it- Thus name immutable ledger.

But building a blockchain system is not enough. It should be decentralized i.e if one server goes down or something happens on a particular node, other nodes can function normally and do not have to wait for the victim node’s recovery.

So a gist of advantages are listed below:
- You can vote anytime/anywhere (During Pandemics like COVID-19 where it’s impossible to hold elections physically)
- Secure
- Immutable
- Faster
- Transparent

## Let’s visualize the process

It is always interesting to learn things if it’s visually explained. Hence the diagram given below explains how the blockchain voting works.

![Blockchain Voting Process](https://media.geeksforgeeks.org/wp-content/uploads/20200424190016/2020-04-22-21.png)

According to the above diagram, the voter needs to enter his/her credentials in order to vote. All data is then encrypted and stored as a transaction. This transaction is then broadcasted to every node in the network, which in turn is then verified. If the network approves the transaction, it is stored in a block and added to the chain. Note that once a block is added to the chain, it stays there forever and can’t be updated. Users can now see results and also trace back the transaction if they want.

Since current voting systems don’t suffice to the security needs of the modern generation, there is a need to build a system that leverages security, convenience, and trust involved in the voting process. Hence voting systems make use of Blockchain technology to add an extra layer of security and encourage people to vote from any time, anywhere without any hassle and makes the voting process more cost-effective and time-saving.


   <h2>Technologies</h2><br>
  <ul><li>Aadhaar API service (for biometric authentication)</li>
    <li>Python (to communicate with blockchain and for backend and frontend API calls)</li>
    <li>Ganache (to create private blockchain network for testing on localhost)</li>
    <li>Flask (web framework)</li>
  </ul>
  
## Routes

- `/login`: User login route. Generates a unique vote ID using Aadhar number and timestamp.
- `/vote`: Voting route. Allows users to select a candidate and submit their vote to the blockchain.
- `/admin`: Admin login route. Checks if the user is an admin.
- `/results`: Admin-only route to view voting results.
- `/verify`: Route to verify a vote using the vote ID.
- `/thank-you`: Thank you page after voting.
- Error handlers for 404 and 500 errors.

## Environment Variables

The following environment variables need to be set in the `.env` file:
- `FLASK_SECRET_KEY`
- `BLOCKCHAIN_RPC_URL`
- `CONTRACT_ADDRESS`
- `CONTRACT_ABI`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `FLASK_DEBUG`