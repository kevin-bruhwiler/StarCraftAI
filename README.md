# StarCraftAI
A StarCraft Broodwar AI that has a heirarchial model structure.  

## Macro
The macro decsion making has two aspects. 

The first uses TensorFlow for the heavy lifting. The TF model's input is the current game state (everything that is known about the game). 
The output of the TF model is the desired game state that the model wishes to take the game. The game state's do not need to be adjacent.
To find an optimal trajectory from the current game state to the desired game state, a genetic algorithm is used. 

## Micro
Not implemented yet. Looking for a developer to help me with this.

## Getting Started

Getting this project up and running is fairly straight forward. There is no additional steps beyond setting up the dependencies.

### Prerequisites

This project depends on the following


* StarCraft: BroodWar 1.16.1
* BWAPI [Source](https://github.com/bwapi/bwapi)
* CyBW [Source](https://bitbucket.org/ratiotile/cybw)

### Installing

Follow the BWAPI's and CyBW's documentation on how to install and configure everything. 

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* *Michael Park* - *Main Developer* - [Github](https://github.com/TuringsEgo)
* *No No* - *Second Developer* - [Github](https://github.com/no0no)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
