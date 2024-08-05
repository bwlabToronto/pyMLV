#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <iostream>
#include <deque>
#include <queue>
#include <vector>
#include <list>
#include <map>

using namespace std;
namespace py = pybind11;

/*************************************************************/

/******************************************************************************/   

class Order_node
{
public:
    double energy;
    int region1;
    int region2;

    Order_node() { energy = 0.0; region1 = 0; region2 = 0; }

    Order_node(const double& e, const int& rregion1, const int& rregion2)
    {
        energy = e;
        region1 = rregion1;
        region2 = rregion2;
    }

    ~Order_node() {}
    // LEXICOGRAPHIC ORDER on priority queue: (energy,label)
    bool operator < (const Order_node& x) const { return ((energy > x.energy) || ((energy == x.energy) && (region1 > x.region1)) || ((energy == x.energy) && (region1 == x.region1) && (region2 > x.region2))); }
};

/******************************************************************************/   

class Neighbor_Region
{
public:
    double energy;
    double total_pb;
    double bdry_length;

    Neighbor_Region() { energy = 0.0; total_pb = 0.0; bdry_length = 0.0; }

    Neighbor_Region(const Neighbor_Region& v) { energy = v.energy; total_pb = v.total_pb; bdry_length = v.bdry_length; }

    Neighbor_Region(const double& en, const double& tt, const double& bor)
    {
        energy = en;
        total_pb = tt;
        bdry_length = bor;
    }

    ~Neighbor_Region() {}

};

/******************************************************************************/   

class Bdry_element
{
public:
    int coord;
    int cc_neigh;

    Bdry_element() {}

    Bdry_element(const int& c, const int& v) { coord = c; cc_neigh = v; }

    Bdry_element(const Bdry_element& n) { coord = n.coord; cc_neigh = n.cc_neigh; }

    ~Bdry_element() {}

    bool operator ==(const Bdry_element& n) const { return ((coord == n.coord) && (cc_neigh == n.cc_neigh)); }
    // LEXICOGRAPHIC ORDER: (cc_neigh, coord)
    bool operator < (const Bdry_element& n) const { return ((cc_neigh < n.cc_neigh) || ((cc_neigh == n.cc_neigh) && (coord < n.coord))); }

};

/******************************************************************************/   

class Region
{
public:
    list<int> elements;
    map<int, Neighbor_Region, less<int>> neighbors;
    list<Bdry_element> boundary;

    Region() {}

    Region(const int& l) { elements.push_back(l); }

    ~Region() {}

    void merge(Region& r, int* labels, const int& label, double* ucm, const double& saliency, const int& son, const int& tx);
};

void Region::merge(Region& r, int* labels, const int& label, double* ucm, const double& saliency, const int& son, const int& tx)
{
    /* I. BOUNDARY */

    // Ia. update father's boundary
    list<Bdry_element>::iterator itrb, itrb2;
    itrb = boundary.begin();
    while (itrb != boundary.end())
    {
        if (labels[(*itrb).cc_neigh] == son)
        {
            itrb2 = itrb;
            ++itrb;
            boundary.erase(itrb2);
        }
        else ++itrb;
    }

    int coord_contour;

    // Ib. move son's boundary to father
    for (itrb = r.boundary.begin(); itrb != r.boundary.end(); ++itrb)
    {
        if (ucm[(*itrb).coord] < saliency) ucm[(*itrb).coord] = saliency;

        if (labels[(*itrb).cc_neigh] != label)
            boundary.push_back(Bdry_element(*itrb));

    }
    r.boundary.erase(r.boundary.begin(), r.boundary.end());

    /* II. ELEMENTS */

    for (list<int>::iterator p = r.elements.begin(); p != r.elements.end(); ++p) labels[*p] = label;
    elements.insert(elements.begin(), r.elements.begin(), r.elements.end());
    r.elements.erase(r.elements.begin(), r.elements.end());

    /* III. NEIGHBORS */

    map<int, Neighbor_Region, less<int>>::iterator itr, itr2;

    // IIIa. remove inactive neighbors from father
    itr = neighbors.begin();
    while (itr != neighbors.end())
    {
        if (labels[(*itr).first] != (*itr).first)
        {
            itr2 = itr;
            ++itr;
            neighbors.erase(itr2);
        }
        else ++itr;
    }

    // IIIb. remove inactive neighbors from son and neighbors belonging to father
    itr = r.neighbors.begin();
    while (itr != r.neighbors.end())
    {
        if ((labels[(*itr).first] != (*itr).first) || (labels[(*itr).first] == label))
        {
            itr2 = itr;
            ++itr;
            r.neighbors.erase(itr2);
        }
        else ++itr;
    }
}

/*************************************************************/

void complete_contour_map(double* ucm, const int& txc, const int& tyc)
/* complete contour map by max strategy on Khalimsky space  */
{
    int vx[4] = { 1, 0, -1,  0 };
    int vy[4] = { 0, 1,  0, -1 };
    int nxp, nyp, cv;
    double maximo;

    for (int x = 0; x < txc; x = x + 2) for (int y = 0; y < tyc; y = y + 2)
    {
        maximo = 0.0;
        for (int v = 0; v < 4; v++)
        {
            nxp = x + vx[v]; nyp = y + vy[v]; cv = nxp + nyp * txc;
            if ((nyp >= 0) && (nyp < tyc) && (nxp < txc) && (nxp >= 0) && (maximo < ucm[cv]))
                maximo = ucm[cv];
        }
        ucm[x + y * txc] = maximo;
    }

}

/***************************************************************************************************************************/
void compute_ucm(double* local_boundaries, int* initial_partition, const int& totcc, double* ucm, const int& tx, const int& ty)
{
    // I. INITIATE
    int p, c;
    int* labels = new int[totcc];

    for (c = 0; c < totcc; c++)
    {
        labels[c] = c;
    }

    // II. ULTRAMETRIC
    Region* R = new Region[totcc];
    priority_queue<Order_node, vector<Order_node>, less<Order_node>> merging_queue;
    double totalPb, totalBdry, dissimilarity;
    int v, px;

    for (p = 0; p < (2 * tx + 1) * (2 * ty + 1); p++) ucm[p] = 0.0;

    // INITIATE REGIONS
    for (c = 0; c < totcc; c++) R[c] = Region(c);

    // INITIATE UCM
    int vx[4] = { 1, 0, -1,  0 };
    int vy[4] = { 0, 1,  0, -1 };
    int nxp, nyp, cnp, xp, yp, label;

    for (p = 0; p < tx * ty; p++)
    {
        xp = p % tx; yp = p / tx;
        for (v = 0; v < 4; v++)
        {
            nxp = xp + vx[v]; nyp = yp + vy[v]; cnp = nxp + nyp * tx;
            if ((nyp >= 0) && (nyp < ty) && (nxp < tx) && (nxp >= 0) && (initial_partition[cnp] != initial_partition[p]))
                R[initial_partition[p]].boundary.push_back(Bdry_element((xp + nxp + 1) + (yp + nyp + 1) * (2 * tx + 1), initial_partition[cnp]));
        }
    }

    // INITIATE merging_queue
    list<Bdry_element>::iterator itrb;
    for (c = 0; c < totcc; c++)
    {
        R[c].boundary.sort();

        label = (*R[c].boundary.begin()).cc_neigh;
        totalBdry = 0.0;
        totalPb = 0.0;

        for (itrb = R[c].boundary.begin(); itrb != R[c].boundary.end(); ++itrb)
        {
            if ((*itrb).cc_neigh == label)
            {
                totalBdry++;
                totalPb += local_boundaries[(*itrb).coord];
            }
            else
            {
                R[c].neighbors[label] = Neighbor_Region(totalPb / totalBdry, totalPb, totalBdry);
                if (label > c)   merging_queue.push(Order_node(totalPb / totalBdry, c, label));
                label = (*itrb).cc_neigh;
                totalBdry = 1.0;
                totalPb = local_boundaries[(*itrb).coord];
            }

        }
        R[c].neighbors[label] = Neighbor_Region(totalPb / totalBdry, totalPb, totalBdry);
        if (label > c)   merging_queue.push(Order_node(totalPb / totalBdry, c, label));
    }


    //MERGING
    Order_node minor;
    int father, son;
    map<int, Neighbor_Region, less<int>>::iterator itr;
    double current_energy = 0.0;

    while (!merging_queue.empty())
    {
        minor = merging_queue.top(); merging_queue.pop();
        if ((labels[minor.region1] == minor.region1) && (labels[minor.region2] == minor.region2) &&
            (minor.energy == R[minor.region1].neighbors[minor.region2].energy))
        {
            current_energy = minor.energy;
            dissimilarity = R[minor.region1].neighbors[minor.region2].total_pb / R[minor.region1].neighbors[minor.region2].bdry_length;

            if (minor.region1 < minor.region2)
            {
                son = minor.region1; father = minor.region2;
            }
            else
            {
                son = minor.region2; father = minor.region1;
            }

            R[father].merge(R[son], labels, father, ucm, dissimilarity, son, tx);

            // move and update neighbors
            while (R[son].neighbors.size() > 0)
            {
                itr = R[son].neighbors.begin();

                R[father].neighbors[(*itr).first].total_pb += (*itr).second.total_pb;
                R[(*itr).first].neighbors[father].total_pb += (*itr).second.total_pb;

                R[father].neighbors[(*itr).first].bdry_length += (*itr).second.bdry_length;
                R[(*itr).first].neighbors[father].bdry_length += (*itr).second.bdry_length;

                R[son].neighbors.erase(itr);
            }

            // update merging_queue
            for (itr = R[father].neighbors.begin(); itr != R[father].neighbors.end(); ++itr)
            {

                dissimilarity = R[father].neighbors[(*itr).first].total_pb / R[father].neighbors[(*itr).first].bdry_length;

                merging_queue.push(Order_node(dissimilarity, (*itr).first, father));
                R[father].neighbors[(*itr).first].energy = dissimilarity;
                R[(*itr).first].neighbors[father].energy = dissimilarity;

            }
        }
    }

    complete_contour_map(ucm, 2 * tx + 1, 2 * ty + 1);

    delete[] R; delete[] labels;
}

/*************************************************************************************************/
py::array_t<double> compute_ucm_py(py::array_t<double> local_boundaries, py::array_t<int> initial_partition) {
    py::buffer_info buf_local_boundaries = local_boundaries.request();
    py::buffer_info buf_initial_partition = initial_partition.request();

    if (buf_local_boundaries.ndim != 2 || buf_initial_partition.ndim != 2) {
        throw std::runtime_error("Input should be 2-D NumPy arrays");
    }

    int tx = buf_initial_partition.shape[0];
    int ty = buf_initial_partition.shape[1];
    int totcc = -1;

    double* local_boundaries_ptr = static_cast<double*>(buf_local_boundaries.ptr);
    int* initial_partition_ptr = static_cast<int*>(buf_initial_partition.ptr);

    for (int px = 0; px < tx * ty; px++) {
        if (totcc < initial_partition_ptr[px]) totcc = initial_partition_ptr[px];
    }
    if (totcc < 0) throw std::runtime_error("ERROR: number of connected components < 0");
    totcc++;

    py::array_t<double> ucm = py::array_t<double>({2 * tx + 1, 2 * ty + 1});
    py::buffer_info buf_ucm = ucm.request();
    double* ucm_ptr = static_cast<double*>(buf_ucm.ptr);

    compute_ucm(local_boundaries_ptr, initial_partition_ptr, totcc, ucm_ptr, tx, ty);

    return ucm;
}

PYBIND11_MODULE(ucm_mean_pb, m) {
    m.def("compute_ucm", &compute_ucm_py, "Compute ultrametric contour maps",
          py::arg("local_boundaries"), py::arg("initial_partition"));
}
