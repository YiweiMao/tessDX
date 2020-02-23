# tessDX
tessellation playground for the [DX11 tessellation spec](https://github.com/microsoft/DirectX-Specs/blob/master/d3d/archive/images/d3d11)

# example usage
```bash
git clone https://github.com/YiweiMao/tessDX
cd tessDX/
make
```

```python
from pytess import *
%matplotlib inline
# if not using jupyter notebook, add this at the end of the script: plt.show()

# for one instance of tessellation
Tessellator(partition=PART_INT,outputPrim=OUTPUT_TRIANGLE_CW,tfs=[1,2,3,4]).doTess()

# for interactivity
interact(showTess,partition=(0,3,1),outputPrim=(0,3,1),outTF0=(1,64,0.1),outTF1=(-1,64,0.1),
                 outTF2=(-1,64,0.01),outTF3=(-1,64,0.1),inTF0=(1,64,0.1),inTF1=(-1,64,0.1))
```

