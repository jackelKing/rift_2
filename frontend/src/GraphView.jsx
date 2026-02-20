import React from "react";
import ForceGraph2D from "react-force-graph-2d";
import { useNavigate } from "react-router-dom";
import NairaButton from "./NairaButton";

export default function GraphView({ analysisResult }) {
  const navigate = useNavigate();

  if (!analysisResult || !analysisResult.fraud_rings) {
    return (
      <div style={{ padding: "40px", color: "white" }}>
        <h2>No Graph Data Available</h2>
        <NairaButton text="Go Back" icon="←" onClick={() => navigate("/results")} />
      </div>
    );
  }

  const fraud_rings = analysisResult.fraud_rings || [];
  const suspicious_accounts = analysisResult.suspicious_accounts || [];

  const nodesMap = {};
  const links = [];

  const suspicionMap = {};
  suspicious_accounts.forEach(acc => {
    suspicionMap[acc.account_id] = acc.suspicion_score || 10;
  });

  fraud_rings.forEach(ring => {
    const members = ring.member_accounts || [];
    const pattern = (ring.pattern_type || "").toLowerCase();

    // Create nodes
    members.forEach(acc => {
      if (!nodesMap[acc]) {
        nodesMap[acc] = {
          id: acc,
          suspicion: suspicionMap[acc] || 10,
          pattern,
          ring_id: ring.ring_id
        };
      }
    });

    // Cycle Rings
    if (pattern.includes("cycle")) {
      for (let i = 0; i < members.length; i++) {
        links.push({
          source: members[i],
          target: members[(i + 1) % members.length],
          type: "cycle"
        });
      }
    }

    // Fan structures
    else if (pattern.includes("fan")) {
      const hub = members[0];
      members.slice(1).forEach(m => {
        links.push({
          source: hub,
          target: m,
          type: "fan"
        });
      });
    }

    // Shell layering
    else if (pattern.includes("shell")) {
      for (let i = 0; i < members.length - 1; i++) {
        links.push({
          source: members[i],
          target: members[i + 1],
          type: "shell"
        });
      }
    }
  });

  const graphData = {
    nodes: Object.values(nodesMap),
    links
  };

  return (
    <div style={{ height: "100vh", background: "#0b0f1a" }}>
      <ForceGraph2D
        graphData={graphData}
        linkDirectionalArrowLength={8}
        linkDirectionalArrowRelPos={1}
        linkWidth={2}
        linkColor={link => {
          if (link.type === "cycle") return "#ff8c00";
          if (link.type === "fan") return "#ffff00";
          if (link.type === "shell") return "#9b59b6";
          return "#888";
        }}
        nodeCanvasObject={(node, ctx) => {
          const risk = node.suspicion || 10;
          const size = Math.max(6, risk / 8);

          let color = "#3498db";

          if (risk > 85) color = "#ff0000";
          else if (node.pattern.includes("cycle")) color = "#ff8c00";
          else if (node.pattern.includes("fan")) color = "#ffff00";
          else if (node.pattern.includes("shell")) color = "#9b59b6";

          ctx.beginPath();
          ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
          ctx.fillStyle = color;
          ctx.fill();
        }}
        nodeLabel={node =>
          `Account: ${node.id}
Suspicion: ${node.suspicion}
Ring: ${node.ring_id}
Pattern: ${node.pattern}`
        }
        cooldownTicks={120}
      />
    </div>
  );
}