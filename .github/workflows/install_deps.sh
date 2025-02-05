#!/bin/sh

# Install CI dependencies, arguments specify what is required

# Base packages
pip install --upgrade pip
pip install wheel setuptools

# Used to create local test environments
pip install tox

# Update apt
sudo apt-get update

# Check arguments
for par in "$@"; do
  case $par in
    doc)
      # documentation
      sudo apt-get install pandoc
    ;;

    amici)
      # for amici
      sudo apt-get install \
        swig libatlas-base-dev libhdf5-serial-dev
    ;;

    ipopt)
      # for ipopt
      sudo apt-get install \
	build-essential \
        coinor-libipopt1v5 coinor-libipopt-dev \
        gfortran lcov pkg-config python-dev zlib1g-dev
    ;;

    pysb)
      # bionetgen
      wget -q -O bionetgen.tar \
        https://github.com/RuleWorld/bionetgen/releases/download/BioNetGen-2.6.0/BioNetGen-2.6.0-linux.tgz
      tar -xf bionetgen.tar
    ;;

    mpi)
      # mpi
      sudo apt-get install libopenmpi-dev
    ;;

    *)
      echo "Unknown argument: $par" >&2
      exit 1
    ;;
  esac
done
