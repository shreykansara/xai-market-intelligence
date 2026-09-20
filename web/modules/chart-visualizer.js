/**
 * Omniscope AI - Chart Visualizer Module
 * Handles HTML5 Canvas Radar Rendering for PESTLE (6-axis) & Porter's 5 Forces (5-axis).
 * Designed with an institutional financial palette (Cobalt & Slate).
 */

export class ChartVisualizer {
    static drawPestleCanvas(canvasObj, vector, peerVector = null) {
        if (!canvasObj) return;
        const ctx = canvasObj.getContext('2d');
        const width = canvasObj.width;
        const height = canvasObj.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 36;
        const labels = ['Political', 'Economic', 'Social', 'Tech', 'Legal', 'Enviro'];
        const numAxes = labels.length;

        ctx.clearRect(0, 0, width, height);

        // Concentric grid circles (subtle slate guidelines)
        for (let level = 1; level <= 4; level++) {
            const r = (radius / 4) * level;
            ctx.beginPath();
            ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.07)';
            ctx.lineWidth = 1;
            ctx.stroke();
        }

        // Axes & Axis Labels
        for (let i = 0; i < numAxes; i++) {
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            ctx.lineWidth = 1;
            ctx.stroke();

            const lx = centerX + Math.cos(angle) * (radius + 20);
            const ly = centerY + Math.sin(angle) * (radius + 20);
            ctx.font = '500 11px Inter, sans-serif';
            ctx.fillStyle = '#94A3B8';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(labels[i], lx, ly);
        }

        // Peer Vector Polygon (Slate dashed overlay)
        if (peerVector && peerVector.length >= numAxes) {
            ctx.beginPath();
            for (let i = 0; i < numAxes; i++) {
                const val = peerVector[i] || 0.3;
                const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
                const r = radius * val;
                const x = centerX + Math.cos(angle) * r;
                const y = centerY + Math.sin(angle) * r;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fillStyle = 'rgba(148, 163, 184, 0.14)';
            ctx.fill();
            ctx.strokeStyle = '#94A3B8';
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // User Vector Polygon (Executive Cobalt Blue)
        ctx.beginPath();
        for (let i = 0; i < numAxes; i++) {
            const val = vector[i] || 0.3;
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const r = radius * val;
            const x = centerX + Math.cos(angle) * r;
            const y = centerY + Math.sin(angle) * r;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = 'rgba(59, 130, 246, 0.22)';
        ctx.fill();
        ctx.strokeStyle = '#3B82F6';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    static drawPorterCanvas(canvasObj, vector, peerVector = null) {
        if (!canvasObj) return;
        const ctx = canvasObj.getContext('2d');
        const width = canvasObj.width;
        const height = canvasObj.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 36;
        const labels = ['New Entrants', 'Buyer Power', 'Supplier Power', 'Substitutes', 'Rivalry'];
        const numAxes = labels.length;

        ctx.clearRect(0, 0, width, height);

        // Concentric grid circles (subtle slate guidelines)
        for (let level = 1; level <= 4; level++) {
            const r = (radius / 4) * level;
            ctx.beginPath();
            ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.07)';
            ctx.lineWidth = 1;
            ctx.stroke();
        }

        // Axes & Axis Labels
        for (let i = 0; i < numAxes; i++) {
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            ctx.lineWidth = 1;
            ctx.stroke();

            const lx = centerX + Math.cos(angle) * (radius + 20);
            const ly = centerY + Math.sin(angle) * (radius + 20);
            ctx.font = '500 11px Inter, sans-serif';
            ctx.fillStyle = '#94A3B8';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(labels[i], lx, ly);
        }

        // Peer Vector Polygon (Slate dashed overlay)
        if (peerVector && peerVector.length >= numAxes) {
            ctx.beginPath();
            for (let i = 0; i < numAxes; i++) {
                const val = peerVector[i] || 0.3;
                const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
                const r = radius * val;
                const x = centerX + Math.cos(angle) * r;
                const y = centerY + Math.sin(angle) * r;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fillStyle = 'rgba(148, 163, 184, 0.14)';
            ctx.fill();
            ctx.strokeStyle = '#94A3B8';
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // User Vector Polygon (Executive Cobalt Blue)
        ctx.beginPath();
        for (let i = 0; i < numAxes; i++) {
            const val = vector[i] || 0.3;
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const r = radius * val;
            const x = centerX + Math.cos(angle) * r;
            const y = centerY + Math.sin(angle) * r;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = 'rgba(59, 130, 246, 0.22)';
        ctx.fill();
        ctx.strokeStyle = '#3B82F6';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    static updateCvpLegendValues(pestleVec, porterVec) {
        if (!pestleVec || !porterVec) return;
        const full11D = [...pestleVec, ...porterVec];
        for (let i = 0; i < 11; i++) {
            const val = (full11D[i] !== undefined ? full11D[i] : 0.35).toFixed(2);
            const mainEl = document.getElementById(`val-p${i}`);
            if (mainEl) mainEl.textContent = val;
            const sideEl = document.getElementById(`sidebar-val-p${i}`);
            if (sideEl) sideEl.textContent = val;
        }
    }

    static updateSalesLegendValues(pestleVec, porterVec) {
        if (!pestleVec || !porterVec) return;
        const full11D = [...pestleVec, ...porterVec];
        for (let i = 0; i < 11; i++) {
            const val = (full11D[i] !== undefined ? full11D[i] : 0.35).toFixed(2);
            const mainEl = document.getElementById(`val-rev-p${i}`);
            if (mainEl) mainEl.textContent = val;
            const sideEl = document.getElementById(`sidebar-val-p${i}`);
            if (sideEl) sideEl.textContent = val;
        }
    }

    static updateLegendValues(prefix, vec) {
        for (let i = 0; i < vec.length; i++) {
            const el = document.getElementById(`${prefix}${i}`);
            if (el) el.textContent = (vec[i] !== undefined ? vec[i] : 0.35).toFixed(2);
        }
    }
}
