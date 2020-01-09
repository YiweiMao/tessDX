#include <stdio.h>
#include "tessellator.hpp"

int main(void) { //int argc, char** argv) {

    int partitionScheme;
    int outputPrimitive;
    int domain;
    int numTFs;
    float tfs[6] = {0};

    FILE *fp;
    fp = fopen("settings.txt", "r");
    fscanf(fp, "%d", &partitionScheme);
    fscanf(fp, "%d", &outputPrimitive);
    fscanf(fp, "%d", &domain);
    fscanf(fp, "%d", &numTFs);

    for (int i=0; i <numTFs; i++) {
        fscanf(fp, "%f", &tfs[i]);
    }
    fclose(fp);

    CHWTessellator hwTess;
    hwTess.Init((D3D11_TESSELLATOR_PARTITIONING)partitionScheme,(D3D11_TESSELLATOR_OUTPUT_PRIMITIVE)outputPrimitive);

    switch (domain)
    {
    case 0:
        hwTess.TessellateIsoLineDomain(tfs[0],tfs[1]);
        break;
    case 1:
        hwTess.TessellateTriDomain(tfs[0],tfs[1],tfs[2],tfs[3]);
        break;
    case 2:
        hwTess.TessellateQuadDomain(tfs[0],tfs[1],tfs[2],tfs[3],tfs[4],tfs[5]);
        break;
    default:
        break;
    }

    fp = fopen("points.csv", "w");
    //printf("get point count is %d\n",hwTess.GetPointCount());
    for(int i=0;i<hwTess.GetPointCount();i++){
        //printf("%.2f,%.2f\t",hwTess.m_Point[i].u,hwTess.m_Point[i].v);
        fprintf(fp,"%.16f,%.16f\n",hwTess.m_Point[i].u,hwTess.m_Point[i].v);
    }
    fclose(fp);

    fp = fopen("indexes.csv", "w");
    //printf("\nget index count is %d\n",hwTess.GetIndexCount());
    for(int i=0;i<hwTess.GetIndexCount();i++){
        //printf("%d\t",hwTess.m_Index[i]);
        fprintf(fp,"%d\n",hwTess.m_Index[i]);
    }
    fclose(fp);

    return 0;
}