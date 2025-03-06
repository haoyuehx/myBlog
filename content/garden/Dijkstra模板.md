---
title: "Dijkstra模板"
date: 2025-03-05
lastmod: 2025-03-05
draft: false
garden_tags: ["图论", "algorithm"]
summary: " "
status: "evergreen"
---

```c++
#include <iostream>
#include <limits>
#include <queue>
#include <stack>
#include <vector>

using namespace std;

struct DirectedEdge {
    int from, to;
    double weight;
    DirectedEdge(int f, int t, double w)
        : from(f)
        , to(t)
        , weight(w)
    {
    }
};

class EdgeWeightedDigraph {
public:
    vector<vector<DirectedEdge>> adj;
    EdgeWeightedDigraph(int V)
        : adj(V + 1)
    {
    } // 1-based index, so size = V+1

    void addEdge(int v, int w, double weight)
    {
        adj[v].emplace_back(v, w, weight);
    }

    int V() const { return adj.size() - 1; } // Ignore index 0
};

class DijkstraSP {
private:
    vector<DirectedEdge*> edgeTo;
    vector<double> distTo;
    priority_queue<pair<double, int>, vector<pair<double, int>>, greater<pair<double, int>>> pq;

public:
    DijkstraSP(const EdgeWeightedDigraph& G, int s)
        : edgeTo(G.V() + 1, nullptr)
        , distTo(G.V() + 1, numeric_limits<double>::infinity())
    {
        distTo[s] = 0.0;
        pq.emplace(0.0, s);
        while (!pq.empty()) {
            int v = pq.top().second;
            pq.pop();
            relax(G, v);
        }
    }

    void relax(const EdgeWeightedDigraph& G, int v)
    {
        for (const auto& e : G.adj[v]) {
            int w = e.to;
            if (distTo[w] > distTo[v] + e.weight) {
                distTo[w] = distTo[v] + e.weight;
                edgeTo[w] = new DirectedEdge(e);
                pq.emplace(distTo[w], w);
            }
        }
    }

    double distToVertex(int v) const
    {
        return distTo[v];
    }

    bool hasPathTo(int v) const
    {
        return distTo[v] < numeric_limits<double>::infinity();
    }

    vector<DirectedEdge> pathTo(int v)
    {
        if (!hasPathTo(v))
            return {};
        stack<DirectedEdge> pathStack;
        for (DirectedEdge* e = edgeTo[v]; e != nullptr; e = edgeTo[e->from]) {
            pathStack.push(*e);
        }
        vector<DirectedEdge> path;
        while (!pathStack.empty()) {
            path.push_back(pathStack.top());
            pathStack.pop();
        }
        return path;
    }
};

int main()
{
    int V, E, s;
    cin >> V >> E >> s;
    EdgeWeightedDigraph G(V);

    for (int i = 0; i < E; i++) {
        int v, w;
        double weight;
        cin >> v >> w >> weight;
        G.addEdge(v, w, weight);
    }

    DijkstraSP sp(G, s);

    for (int t = 1; t <= V; t++) {
        cout << s << " to " << t << " (" << sp.distToVertex(t) << "): ";
        if (sp.hasPathTo(t)) {
            for (const auto& e : sp.pathTo(t)) {
                cout << e.from << "->" << e.to << "(" << e.weight << ")  ";
            }
        }
        cout << endl;
    }

    return 0;
}
```
