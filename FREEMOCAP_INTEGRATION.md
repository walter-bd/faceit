# FaceIt + FreeMocap Integration Guide

Complete workflow for combining full-body motion capture (FreeMocap) with facial animation (FaceIt) in Blender.

## Overview

**FreeMocap**: Open-source full-body motion capture system. Captures skeletal data from multi-camera setups and exports to Blender as armatures (BVH/FBX).

**FaceIt**: Blender addon for facial rigging and real-time mocap (Face Cap, Live Link Face, OSC, iFacialMocap). Handles shape keys and facial bone animation.

**Combined**: Full-character animation with synchronized body movement and facial expressions.

## System Architecture

```
FreeMocap (Body)          FaceIt (Face)
    ↓                         ↓
  BVH/FBX              OSC/Live Stream
    ↓                         ↓
  Skeleton Rig      →  Facial Rig
    ↓                         ↓
      └─────→ Blender Character ←─────┘
```

## Installation

### Prerequisites

- Blender 4.5+ (tested with 4.5.5)
- Python 3.9+
- Basic understanding of rigging, bone structure, shape keys

### Step 1: Install FreeMocap

```bash
# Install from conda (recommended)
conda install -c conda-forge freemocap

# Or pip
pip install freemocap
```

**Verify installation:**
```bash
freemocap --version
```

### Step 2: Install FreeMocap Blender Addon

Download from: https://github.com/freemocap/freemocap_blender_addon

In Blender:
1. Edit → Preferences → Add-ons
2. Install → select freemocap_blender_addon folder
3. Search "FreeMocap" and enable
4. Restart Blender

### Step 3: Install FaceIt Addon

Download from: https://github.com/yourusername/faceit (your repo)

In Blender:
1. Edit → Preferences → Add-ons
2. Install → select faceit folder
3. Search "FACEIT" and enable
4. Verify in Animate tab → FaceIt panel appears

## Workflow: Recording

### Full-Body Motion (FreeMocap)

1. **Set up camera array** (2+ webcams minimum, recommended 4+)
   - Mount cameras around actor in circle
   - Ensure good lighting, clear background
   - Calibrate using FreeMocap's calibration tools

2. **Record session**
   ```bash
   freemocap record --camera-array
   ```

3. **Process recording**
   - FreeMocap auto-processes after recording
   - Generates `.npy` files with 3D joint positions
   - Creates skeleton in output folder

### Facial Motion (FaceIt)

**Option A: Live Capture with Face Cap App**
1. Install Face Cap on iPhone/iPad
2. Connect to same network as Blender machine
3. In FaceIt panel → Mocap section → Select "Face Cap"
4. Enable OSC Receiver
5. Hit Record in Blender

**Option B: Live Link Face (Epic)**
1. Install Live Link Face app (iPhone/iPad)
2. Blender machine on same network
3. FaceIt panel → Select "Live Link Face"
4. Enable receiver, record

**Option C: Pre-recorded Video**
1. Record facial performance on camera
2. Use external facial mocap tool (MediaPipe, etc.)
3. Import data into FaceIt via OSC or manual keyframing

## Workflow: Blender Assembly

### Phase 1: Import FreeMocap Data

1. **Load FreeMocap recording**
   - Create new Blender project
   - Animate tab → FreeMocap panel
   - Load FreeMocap session folder
   - FreeMocap generates armature with T-pose

2. **Verify skeletal rig**
   - Check bone structure and naming
   - Ensure root bone (usually "root" or "pelvis")
   - Verify foot contact points for motion smoothing

3. **Retarget skeleton (if needed)**
   - If using custom character: use Blender's bone constraint system
   - Parent character mesh to FreeMocap armature using Armature modifier
   - Test with simple bend/walk cycle to verify tracking

### Phase 2: Set Up Character Mesh

1. **Import your character model**
   - Use your existing rigged character or create new one
   - Ensure topology matches your facial rig design

2. **Create facial rig in FaceIt**
   - Select head mesh
   - FaceIt panel → Setup → Create Control Rig
   - Configure shape keys (ARKit 52 blend shapes recommended)
   - Set up bone-based controls if needed

3. **Parent face to body**
   - Head mesh should be child of FreeMocap head bone
   - Verify transform hierarchy:
     ```
     FreeMocap Armature (body)
     └── Head Bone
         └── Character Head Mesh (with FaceIt shapes + bones)
     ```

### Phase 3: Synchronize Timing

**If recording simultaneously:**
- Clap or snap fingers at start of both recordings (sync mark)
- Note frame numbers in both systems
- In Blender, offset one timeline to match (usually FaceIt → shift forward/backward)

**If recording separately:**
- Manual frame offset in Blender Timeline
- Use visual sync: align mouth/lip shapes with audio

**Code for offset (Python Console):**
```python
import bpy
scene = bpy.context.scene

# Shift FaceIt action 120 frames forward
for action in bpy.data.actions:
    if 'faceit' in action.name.lower():
        for fcurve in action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.co.x += 120
```

## Workflow: Animation

### Body Animation (FreeMocap-driven)

FreeMocap automatically generates NLA strips with skeletal animation. Verify:
- Motion quality (no jitter? → smooth with Blender's smoothing tools)
- Foot contact (should stay grounded)
- Hip position (should match character height)

**Refine FreeMocap animation:**
1. Graph Editor → smooth spiky curves (hold Alt, select, S key)
2. Dope Sheet → remove keyframes with bad tracking
3. Use constraints (Pole Target, IK) for limb stabilization if needed

### Facial Animation (FaceIt-driven)

1. **Enable live animation**
   - FaceIt panel → Mocap section → Enable receiver
   - Select shape key target or bone rig
   - Start streaming from Face Cap/Live Link Face

2. **Record facial performance**
   - Play Blender timeline (Spacebar)
   - Perform facial expressions sync'd with body mocap
   - FaceIt records shape key/bone keyframes

3. **Refine facial animation**
   - Graph Editor → Dope Sheet
   - Clean up noise in shape key curves
   - Add secondary expressions (blinks, micro-expressions)
   - Adjust shape key weights for character-specific blending

## Advanced Integration

### Retargeting Different Characters

If body rig doesn't match your character skeleton:

1. **Create Armature Modifier chain**
   - Your character mesh → Armature Modifier → points to custom rig
   - Create custom rig with matching bone structure
   - Use bone constraints (Copy Rotation, Copy Location) to drive custom bones from FreeMocap

2. **Use Constraints**
   ```
   Custom Bone → Copy Rotation constraint → FreeMocap bone
   ```

### Frame-by-Frame Sync

Use Blender's frame markers:
1. Add marker on sync frame (M key in Timeline)
2. Name both markers "SYNC"
3. Offset by moving entire action in NLA editor

### Multi-Camera Angle Export

If recording multiple takes with different setups:
1. Record body mocap each setup
2. Record face mocap once (reuse across setups)
3. Import multiple FreeMocap rigs, parent same facial rig to each

### Exporting Final Animation

1. **Bake combined animation**
   ```
   Select character → Object → Animation → Bake Action
   ```
   This merges FreeMocap skeletal + FaceIt facial into single Action

2. **Export**
   - FBX → includes all armatures, shape keys, actions
   - Alembic → for cloth simulation
   - BVH → skeletal only (loses facial)

## Troubleshooting

### FreeMocap skeleton not tracking well
- Increase camera resolution
- Improve lighting (key light + fill light)
- Check calibration (run FreeMocap calibration dance)
- Ensure clear markers/body visibility

### Facial animation drifting from body
- Check frame sync (Dope Sheet shows both timelines?)
- Verify playback speed matches (24fps? 30fps?)
- Use Blender's time offset modifier on facial action if needed

### Shape keys not responding to mocap
- Verify FaceIt panel shows incoming OSC data
- Check shape key names match expected (ARKit standard?)
- Confirm OSC receiver port (default 9001)
- Check Face Cap/Live Link Face app connection

### Head bone orientation wrong
- Check FreeMocap head bone forward axis
- Rotate armature in pose mode to match character
- Use constraint to fix rotation without changing animation

### Timing sync issues
```python
# Check action frame ranges
import bpy
for action in bpy.data.actions:
    frame_range = action.frame_range
    print(f"{action.name}: {frame_range[0]:.0f} - {frame_range[1]:.0f}")
```

## Performance Tips

1. **Simplify FreeMocap rig** (especially if using all 133 joints)
   - Delete unused bones
   - Keep only: spine, arms, legs, head

2. **Reduce shape key count** (if animation is slow)
   - FaceIt → disable unused shapes
   - Keep essential: mouth (O_U, O_O, A_E), eyes, brows

3. **Use Playblast** instead of viewport to test
   - Faster feedback loop
   - Export to video to check timing without real-time playback

4. **Disable FreeMocap video planes** during animation editing
   - Takes VRAM
   - Use only during reference phase

## Example Project Structure

```
my_project/
├── freemocap_recording/          # FreeMocap output
│   ├── *.npy                      # Skeletal data
│   ├── videos/                    # Source footage
│   └── output.blend               # FreeMocap-generated rig
├── character/
│   ├── character.blend            # Your character model
│   └── character_rigged.blend     # Character + facial rig
└── final/
    └── animation_combined.blend   # FreeMocap + FaceIt merged
```

## Best Practices

1. **Always work non-destructively**
   - Use NLA editor, don't modify original actions
   - Duplicate actions before editing

2. **Name actions clearly**
   - `FreeMocap_body_take01`
   - `FaceIt_face_take01`
   - `Combined_full_take01`

3. **Version control**
   - Keep FreeMocap raw data
   - Keep separate FaceIt facial recordings
   - Only finalize animation in last pass

4. **Test on target platform**
   - Export → Game engine → Verify animation quality
   - Check shape key blending on target character

## Resources

- [FreeMocap GitHub](https://github.com/freemocap/freemocap)
- [FreeMocap Blender Addon](https://github.com/freemocap/freemocap_blender_addon)
- [FaceIt Documentation](https://faceit-doc.readthedocs.io/)
- [Blender Rigging Documentation](https://docs.blender.org/manual/en/latest/animation/armatures/)

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| FreeMocap bones in wrong position | T-pose reference issue | Re-run calibration, check marker visibility |
| Face drifts from body | Timeline misalignment | Use frame markers to sync, offset NLA strips |
| Shape keys jittery | Raw mocap noise | Smooth curves in Graph Editor (hold Alt+S) |
| Head rotates incorrectly | Bone forward axis mismatch | Apply rotation constraint or rotate armature |
| OSC not received | Port blocked/wrong IP | Check FaceIt port (9001), verify network |
| Memory overflow | Too many shapes + high-res video | Delete video planes, disable unneeded shapes |

## Contact & Support

For FaceIt issues: See FaceIt documentation  
For FreeMocap issues: [FreeMocap Discord](https://discord.gg/freemocap)  
For integration questions: Blender Stack Exchange (tag: mocap)
