export default function About() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-extrabold text-white mb-2">About WC 2026</h1>
      <p className="text-slate-400 text-sm mb-8">Your independent FIFA World Cup 2026 tracker</p>

      <div className="space-y-6 text-slate-300 text-sm leading-relaxed">
        <section>
          <h2 className="text-white font-semibold text-lg mb-2">What is this site?</h2>
          <p>WC 2026 is an independent fan-made website dedicated to tracking the 2026 FIFA World Cup, hosted across the United States, Canada, and Mexico from June 11 to July 19, 2026.</p>
          <p className="mt-2">We cover all 48 teams, 12 groups, the full tournament bracket, and in-depth player statistics drawn from the 2025–26 club season across the top football leagues worldwide.</p>
        </section>

        <section>
          <h2 className="text-white font-semibold text-lg mb-2">The 2026 World Cup</h2>
          <p>This edition is historic — it's the first World Cup to feature 48 teams, up from 32. The expanded format introduces 12 groups of 4, with the top 2 from each group plus the 8 best third-placed teams advancing to a new Round of 32.</p>
          <p className="mt-2">104 matches will be played across 16 host cities, with the final taking place on July 19 at MetLife Stadium in East Rutherford, New Jersey.</p>
        </section>

        <section>
          <h2 className="text-white font-semibold text-lg mb-2">Player Statistics</h2>
          <p>Our player stats database covers over 5,500 players from WC 2026 nations, pulling data from the 2025–26 season across 8 major leagues including the Big 5 European leagues, MLS, Liga MX, Eredivisie, Saudi Pro League, Primeira Liga, and the Brazilian and Argentine top flights.</p>
          <p className="mt-2">Key metrics include Expected Goals (xG), Expected Assists (xA), progressive passes, shots on target, tackles, interceptions and more — giving a data-driven view of each team's strength heading into the tournament.</p>
        </section>

        <section>
          <h2 className="text-white font-semibold text-lg mb-2">Disclaimer</h2>
          <p>This site is an independent fan project and is not affiliated with FIFA, any national football association, or any club. All statistics are sourced from publicly available data. Player and team data is provided for informational and entertainment purposes only.</p>
        </section>
      </div>
    </div>
  )
}
