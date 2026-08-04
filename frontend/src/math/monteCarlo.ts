export interface PercentileResult {
  year: number;
  p10: number;
  p50: number;
  p90: number;
}

function randomNormal(): number {
  let u1 = 0, u2 = 0;
  while (u1 === 0) u1 = Math.random();
  while (u2 === 0) u2 = Math.random();
  return Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
}

export function runClientSimulation(
  initialCapital: number,
  annualReturn: number,
  annualVolatility: number,
  years: number,
  simulationsCount: number = 2000
): PercentileResult[] {
  const stepsPerYear = 12;
  const totalSteps = years * stepsPerYear;
  const dt = 1 / stepsPerYear;

  const drift = (annualReturn - 0.5 * Math.pow(annualVolatility, 2)) * dt;
  const vol = annualVolatility * Math.sqrt(dt);

  const trajectories: number[][] = Array.from({ length: totalSteps + 1 }, () => []);
  for (let sim = 0; sim < simulationsCount; sim++) {
    trajectories[0].push(initialCapital);
  }

  for (let step = 1; step <= totalSteps; step++) {
    for (let sim = 0; sim < simulationsCount; sim++) {
      const prev = trajectories[step - 1][sim];
      const z = randomNormal();
      trajectories[step].push(prev * Math.exp(drift + vol * z));
    }
  }

  const results: PercentileResult[] = [];
  for (let year = 0; year <= years; year++) {
    const valuesAtStep = [...trajectories[year * stepsPerYear]].sort((a, b) => a - b);
    results.push({
      year,
      p10: Math.round(valuesAtStep[Math.floor(simulationsCount * 0.10)]),
      p50: Math.round(valuesAtStep[Math.floor(simulationsCount * 0.50)]),
      p90: Math.round(valuesAtStep[Math.floor(simulationsCount * 0.90)]),
    });
  }

  return results;
}