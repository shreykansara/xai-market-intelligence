/**
 * Omniscope AI - Chart Visualizer Module
 * Handles HTML5 Canvas Radar Rendering for PESTLE (6-axis) & Porter's 5 Forces (5-axis).
 */

export class ChartVisualizer {
    static drawPestleCanvas(canvasObj, vector, peerVector = null) {
        if (!canvasObj) return;
        const ctx = canvasObj.getContext('2d');
        const width = canvasObj.width;
        const height = canvasObj.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 35;
        const labels = ['Political', 'Economic', 'Social', 'Tech', 'Legal', 'Enviro'];
        const numAxes = labels.length;

        ctx.clearRect(0, 0, width, height);

        // Grid circles
        for (let level = 1; level <= 4; level++) {
            const r = (radius / 4) * level;
            ctx.beginPath();
            ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            ctx.stroke();
        }

        // Axes & Labels
        for (let i = 0; i < numAxes; i++) {
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            ctx.stroke();

            const lx = centerX + Math.cos(angle) * (radius + 18);
            const ly = centerY + Math.sin(angle) * (radius + 18);
            ctx.font = '10px Inter';
            ctx.fillStyle = '#00FF66';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(labels[i], lx, ly);
        }

        // Peer Vector Polygon (cyan dashed line)
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
            ctx.fillStyle = 'rgba(0, 229, 255, 0.18)';
            ctx.fill();
            ctx.strokeStyle = '#00E5FF';
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // User Vector Polygon (electric green)
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
        ctx.fillStyle = 'rgba(0, 255, 102, 0.28)';
        ctx.fill();
        ctx.strokeStyle = '#00FF66';
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
        const radius = Math.min(centerX, centerY) - 35;
        const labels = ['New Entrants', 'Buyer Power', 'Supplier Power', 'Substitutes', 'Rivalry'];
        const numAxes = labels.length;

        ctx.clearRect(0, 0, width, height);

        // Grid circles
        for (let level = 1; level <= 4; level++) {
            const r = (radius / 4) * level;
            ctx.beginPath();
            ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            ctx.stroke();
        }

        // Axes & Labels
        for (let i = 0; i < numAxes; i++) {
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            ctx.stroke();

            const lx = centerX + Math.cos(angle) * (radius + 18);
            const ly = centerY + Math.sin(angle) * (radius + 18);
            ctx.font = '10px Inter';
            ctx.fillStyle = '#00E5FF';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(labels[i], lx, ly);
        }

        // Peer Vector Polygon (green dashed line)
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
            ctx.fillStyle = 'rgba(0, 255, 102, 0.18)';
            ctx.fill();
            ctx.strokeStyle = '#00FF66';
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // User Vector Polygon (cyan)
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
        ctx.fillStyle = 'rgba(0, 229, 255, 0.28)';
        ctx.fill();
        ctx.strokeStyle = '#00E5FF';
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

