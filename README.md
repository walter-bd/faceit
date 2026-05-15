# FaceIt

A Blender addon for facial rigging, shape key animation, and real-time motion capture integration.

**Version:** 2.3.1  
**License:** GNU General Public License v3

## What It Does

FaceIt provides comprehensive facial animation tools for Blender:

- **Facial Rigging**: Automated setup and control of facial rigs with shape keys and bone-based controls
- **Motion Capture Integration**: Real-time mocap support via:
  - Face Cap App
  - Epic Live Link Face (30fps support)
  - Hallway Tile
  - iFacialMocap
  - OSC (Open Sound Control) protocol
- **Shape Key Management**: Organize and manage face shape keys efficiently
- **Control Rig System**: Create and manage control rigs for facial animation
- **Live Animation**: Animate head position, rotation, and facial expressions in real-time

## Installation

1. Download the addon (this repository)
2. In Blender, go to **Edit → Preferences → Add-ons**
3. Click **Install...** and select the `faceit` folder
4. Search for "FACEIT" and enable the addon
5. The addon panel appears in the **Animate** tab of the 3D Viewport

## Basic Usage

1. **Setup Face Rig**: Select your character mesh and use the FaceIt panel to create/import a face rig
2. **Configure Mocap Source**: In the **Mocap** section, select your motion capture source (Face Cap, Live Link Face, etc.)
3. **Live Animation**: Enable the OSC receiver to stream facial data in real-time
4. **Animate Shapes**: Control shape keys and bone-based facial expressions

For detailed documentation, see: https://faceit-doc.readthedocs.io/en/latest/expressions-2-0/

## Tested Versions

- **Blender 2.80+** (minimum requirement)
- **Blender 4.5.5** (latest tested version)
  - Note: Blender 4.5.5 removed `SoundSequence` type; addon gracefully handles this

## Features

- Shape key-based facial animation
- Bone-based facial rigging
- Real-time OSC mocap streaming
- 30fps Live Link Face support
- Automated control rig setup
- Head animation (location & rotation)
- Audio sequence support (where available)
