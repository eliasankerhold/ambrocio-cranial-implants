<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Cranalyzer</h3>

  <p align="center">
    This repository is being used in the development of novel modular cranial implants. It provides tools for the analysis and visualization of datasets containing 3D models of human skulls with cranial defects. 
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This projects aids the quantitative analysis of cranial defects in humans by providing tools for analyzing datasets of 3D-models of damaged skulls in STL file format. The analysis is based on a ray casting procedure, where linear rays originating from a pre-defined reference skull are intersected with damaged skull models. A visualization tool allows the creation of an interactive 3D-heatmap, which displays the whole database on the surface of the reference skull.

The majority of such databases do not originate from targeted efforts to investigate the statistic of cranial defects, but are a byproduct of patient-specific implant design. Since this design process only requires models of the upper parts of the skull, facial features are commonly not present. This removes almost all symmetries and dramatically complicates the alignment necessary for an analysis. In the current state of the project, it is therefore necessary to manually align the damaged skull models to the reference skull. If the availability of such databases improves, a machine-learning based approach to this alignment procedure could be explored.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This project is fully pip installable, but not hosted on pypi. 

### Prerequisites

To get started, preprocessed and tested resources are available [here](https://drive.google.com/drive/folders/1EVF9dfmyLoLZwhiFuIL9kGNNWUk-N6gN?usp=sharing).

Foremost, the linked directories contain a healthy reference skull on which the analysis was based. The reference skull only consists of the top part and has all facial features removed. There are two versions, one reduced further to only show the left side of the top part.

Additionally, the database contain 29 models of human skulls with cranial defects taken from the publicly available [MUG500+ database](https://github.com/Jianningli/mug500plus). All models are aligned with respect to the reference skull and mirrored in such a way that the defect is on the left side. This was done to improve data quality since a symmetry axis from the front to the back of the skull can be assumed with very good approximation.

*A more detailed description where to save these files to run the example code out of the box will follow here.*

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/eliasankerhold/ambrocio-cranial-implants.git
   ```
2. Navigate to the root directory
   ```sh
   cd ambrocio-cranial-implants
   ```
3. Install using pip
   ```sh
   python -m pip install .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

An example workflow and working analysis of the referenced database can be found in the `examples` directory.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GPLv3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Elias Ankerhold - elias.ankerhold[at]aalto.fi </br>
Jonas Tjepkema - jonas.tjepkema[at]aalto.fi

Project Link: [https://github.com/eliasankerhold/ambrocio-cranial-implants](https://github.com/eliasankerhold/ambrocio-cranial-implants)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
