#include <stdio.h>
#include "tessellator.hpp"

int main(void) {
    printf("Hello World!\n");

    CHWTessellator hwTess;
    hwTess.Init(D3D11_TESSELLATOR_PARTITIONING_FRACTIONAL_EVEN,D3D11_TESSELLATOR_OUTPUT_TRIANGLE_CW);
    hwTess.TessellateTriDomain(1, 1, 1, 3);

    printf("get point count is %d\n",hwTess.GetPointCount());
    for(int i=0;i<hwTess.GetPointCount();i++){
        printf("%.2f,%.2f\t",hwTess.m_Point[i].u,hwTess.m_Point[i].v);
    }

    printf("\nget index count is %d\n",hwTess.GetIndexCount());
    
    for(int i=0;i<hwTess.GetIndexCount();i++){
        printf("%d\t",hwTess.m_Index[i]);
    }

    hwTess.DumpAllPointsAsInOrderLineList();
    printf("\nget index count is %d\n",hwTess.GetIndexCount());
    for(int i=0;i<hwTess.GetIndexCount();i++){
        printf("%d\t",hwTess.m_Index[i]);
    }

    printf("\nHello world again");
    return 0;
}