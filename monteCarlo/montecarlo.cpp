#include <algorithm>
#include <array>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
#include <windows.h>

constexpr int KJØRINGER = 1'000'000;

constexpr int LOGG_INTERVALL = KJØRINGER / 100;

// Funksjoner std
double regnStd(const std::vector<double> &verdier, double snitt) {
  if (verdier.size() <= 1)
    return 0.0;

  double sumKvadrat = 0.0;
  for (double x : verdier)
    sumKvadrat += (x - snitt) * (x - snitt);

  return std::sqrt(sumKvadrat / (verdier.size() - 1)); // Bessel-korr
}

double regnMean(const std::vector<double> &verdier) {
  if (verdier.empty())
    return 0.0;
  return std::accumulate(verdier.begin(), verdier.end(), 0.0) / verdier.size();
}

double regnMedian(std::vector<double> verdier) {
  if (verdier.empty())
    return 0.0;

  std::sort(verdier.begin(), verdier.end());
  const size_t n = verdier.size();

  if (n % 2 == 1)
    return verdier[n / 2];
  else
    return (verdier[n / 2 - 1] + verdier[n / 2]) / 2.0;
}

int main() {
  SetConsoleOutputCP(65001); // legger inn æ, ø, å
  std::setlocale(LC_ALL, ".UTF-8");
  // Hardkodet datasett: antall døde per år (75 år tot). 
  constexpr std::array<int, 75> døde = {
      50,  78,  61,  69,  70,  69,  79,  55,  73,  73,  77,  76,  85,
      72,  78,  103, 88,  75,  84,  93,  118, 115, 93,  84,  101, 104,
      72,  106, 109, 112, 118, 106, 98,  117, 101, 117, 107, 133, 124,
      116, 114, 135, 133, 123, 123, 115, 130, 125, 121, 139, 134, 138,
      119, 124, 124, 132, 133, 118, 115, 119, 137, 141, 128, 127, 137,
      106, 115, 124, 120, 119, 147, 141, 104, 137, 140};

  // lagrer snitt og std én verdi per kjøring. Preallokert for preformance
  std::vector<double> snittPerKjøring;
  snittPerKjøring.reserve(KJØRINGER);
  std::vector<double> stdPerKjøring;
  stdPerKjøring.reserve(KJØRINGER);

  // Random number gen, skal være den raskeste metoden innen normalt STL
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<int> dist(1, 365);

  // Gjenbrukbar buffer for årsgjennomsnitt innad i én kjøring
  std::vector<double> årsSnitt;
  årsSnitt.reserve(døde.size());

  std::cout << "Kjører " << KJØRINGER << " simuleringer...\n";

  for (int i = 0; i < KJØRINGER; ++i) {
    // Logger på pr.prosent. Antar neglisjerbar preformance impact
    if (i % LOGG_INTERVALL == 0) {
      int prosent = (i * 100) / KJØRINGER;
      std::cout << "  " << std::setw(3) << prosent << "% (" << i << " / "
                << KJØRINGER << ")\n";
      std::cout.flush(); // tving utskrift med en gang
    }

    årsSnitt.clear();

    for (int antall : døde) {
      // errorsjekking out of bounds. Litt unødvendig eglig, fordi at datasettet er renset
      // antar neglisjerbar pref imp.
      if (antall <= 0) {
        årsSnitt.push_back(0.0);
        continue;
      }

      // stor pref optimalisering. Vi summerer alle de tilfelige tallene,
      // for å så dele. Dette skal i teorien spare ganske mange instruksjoner mot å
      // ha en dele-operasjoner mot å finne gjennomsnitt 50-150. Hvert år. Hver kjøring. 
      double sum = 0.0;
      for (int k = 0; k < antall; ++k)
        sum += dist(gen);

      årsSnitt.push_back(sum / antall);
    }

    double snitt = regnMean(årsSnitt);
    snittPerKjøring.push_back(snitt);
    stdPerKjøring.push_back(regnStd(årsSnitt, snitt));
  }

  std::cout << "Behandler data...\n\n";

  // Sorter for min/max. Vi gjør dette for å gjøre det lettere å behandle data
  std::sort(snittPerKjøring.begin(), snittPerKjøring.end());
  std::sort(stdPerKjøring.begin(), stdPerKjøring.end());

  const double snittSnitt = regnMean(snittPerKjøring);
  const double medianSnitt = regnMedian(snittPerKjøring);
  const double snittStd = regnMean(stdPerKjøring);
  const double medianStd = regnMedian(stdPerKjøring);
  const double stdNormalkurve = regnStd(snittPerKjøring, snittSnitt); // stdNormalkurve er standardfeilen
  const double seSnitt =
      stdNormalkurve / std::sqrt(static_cast<double>(KJØRINGER));
  const double seStd = regnStd(stdPerKjøring, snittStd) /
                       std::sqrt(static_cast<double>(KJØRINGER));

  std::cout << std::fixed << std::setprecision(9);

  std::cout
      << " -- Gjennomsnittlig dødsdag (1951-2025, per kjøring altså) \n";
  std::cout << "  Snitt:         " << snittSnitt << " dager\n";
  std::cout << "  Median:        " << medianSnitt << " dager\n";
  std::cout << "  Min:           " << snittPerKjøring.front() << " dager\n";
  std::cout << "  Max:           " << snittPerKjøring.back() << " dager\n";
  std::cout << "  Std Gj.Snitt : " << stdNormalkurve << " dager\n";
  std::cout << "  Standardfeil:  " << seSnitt << " dager\n";
  // Om du kjørte alle 30 millioner kjøringer på nytt og beregnet snitt-snitt
  // vill det nye snitt-snitt lande innenfor 183 ± 0.00022 med 68%
  // sannsynlighet.

  std::cout << "\n-- Standardavvik mellom år (innad pr. kjøring)\n";
  std::cout << "  Snitt std:     " << snittStd << " dager\n";
  std::cout << "  Median std:    " << medianStd << " dager\n";
  std::cout << "  Min std:       " << stdPerKjøring.front() << " dager\n";
  std::cout << "  Max std:       " << stdPerKjøring.back() << " dager\n";
  std::cout << "  Standardfeil:  " << seStd << " dager\n";
  // Om du kjørte alle 30 millioner kjøringer på nytt og beregnet snitt-std
  // vill det nye snitt-std lande innenfor 10.4 ± 0.00089 med 68%
  // sannsynlighet.
  return 0;
}
