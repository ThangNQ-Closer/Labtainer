# vp9-parity-coeff-stego

Labtainer lab for **VP9 Directed Parity Coefficient Steganography**.

This lab simulates steganography in the quantized transform coefficient domain of VP9-like video data. It does not modify real VP9/WebM bitstreams and does not include command-and-control, network exfiltration, or malicious payload behavior.

## Learning goals

- Inspect VP9-style quantized transform coefficient data.
- Distinguish DC coefficient `c0` from AC coefficients `c1..c15`.
- Embed a defensive payload with directed parity coding.
- Prefer coefficient changes that reduce absolute magnitude when safe.
- Avoid modifying DC coefficients, zero coefficients, and coefficients that would become zero.
- Extract the hidden message from stego coefficients.
- Perform forensic analysis with coefficient changes, parity distribution, magnitude changes, zero-to-nonzero, nonzero-to-zero, and DC unchanged checks.

## Repository layout

```text
sender/          coefficient generation, inspection, embedding, extraction
analyst/         forensic comparison and statistics scripts
checkwork/       Labtainer checkwork logic
instr_config/    Labtainer grading configuration
dockerfiles/     Labtainer Dockerfiles
docs/            HTML student guide
config/          Labtainer metadata
```

## Run with Labtainer

Copy this directory to:

```bash
~/labtainer/trunk/labs/vp9-parity-coeff-stego
```

Then launch:

```bash
labtainer vp9-parity-coeff-stego
```

Inside the lab, follow the manual at:

```text
file:///home/student/labtainer/trunk/labs/vp9-parity-coeff-stego/docs/vp9-parity-coeff-stego.html
```

## Run standalone with Docker Compose

After the images are published to Docker Hub, edit `docker-compose.yml` and replace `YOUR_DOCKERHUB_USERNAME` with the Docker Hub namespace.

Start the environment:

```bash
docker compose up -d
```

Open sender:

```bash
docker compose exec sender bash
```

Open analyst:

```bash
docker compose exec analyst bash
```

The two containers share data through `/shared`.

## Sender workflow

```bash
python3 make_coefficients.py --output cover_coeffs.csv --frames 30 --blocks-per-frame 120
cp cover_coeffs.csv /shared/

python3 inspect_coeffs.py --input cover_coeffs.csv --output coeff_info.json
cp coeff_info.json /shared/

python3 parity_embed.py \
  --infile cover_coeffs.csv \
  --outfile stego_parity.csv \
  --message "DEFENSIVE-LAB-PAYLOAD-ONLY" \
  --min-abs 2
cp stego_parity.csv embed_report.json /shared/

python3 parity_extract.py \
  --infile stego_parity.csv \
  --output extract_report.json \
  --min-abs 2
cp extract_report.json /shared/
```

## Analyst workflow

```bash
python3 compare_coeffs.py \
  --cover /shared/cover_coeffs.csv \
  --stego /shared/stego_parity.csv \
  --output compare_report.json
cp compare_report.json /shared/

python3 parity_stats.py \
  --infile /shared/stego_parity.csv \
  --output parity_report.json
cp parity_report.json /shared/

python3 magnitude_stats.py \
  --cover /shared/cover_coeffs.csv \
  --stego /shared/stego_parity.csv \
  --output magnitude_report.json
cp magnitude_report.json /shared/
```

## Checkwork expectation

When all required artifacts exist and the JSON reports are valid, Labtainer checkwork should report:

```text
Y - coefficients_created
Y - coefficients_inspected
Y - parity_embedding_completed
Y - message_extracted
Y - magnitude_analyzed
Y - labtainer_outputs_ready
```

## Docker image names

Recommended Docker Hub tags:

```text
YOUR_DOCKERHUB_USERNAME/vp9-parity-coeff-stego-sender:latest
YOUR_DOCKERHUB_USERNAME/vp9-parity-coeff-stego-analyst:latest
```

