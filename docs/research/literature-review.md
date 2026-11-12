# Literature review — 2026-11-12
Purpose: preserve the original research question of reducing unauthorized AI facial cloning without visible redaction. This review does not provide implementation instructions for defeating recognition systems.

## Evidence by threat category
- Single-reference personalization: Song et al., CVPR 2025, IDProtector. Authors report results against several identity-preserving generation systems. This is author-reported evidence, not independent GhostFace validation. [Proceedings](https://openaccess.thecvf.com/content/CVPR2025/html/Song_IDProtector_An_Adversarial_Noise_Encoder_to_Protect_Against_ID-Preserving_Image_CVPR_2025_paper.html).
- Face swapping: Jeong et al., ICCV 2025, FaceShield. Authors evaluate diffusion and GAN-based deepfake generation on two datasets. The reported findings do not establish protection on arbitrary future systems. [Proceedings](https://openaccess.thecvf.com/content/ICCV2025/html/Jeong_FaceShield_Defending_Facial_Image_against_Deepfake_Threats_ICCV_2025_paper.html).
- Image editing: Salman et al., 2023, Raising the Cost of Malicious AI-Powered Image Editing (PhotoGuard). Research concerns editing rather than a general guarantee against identity cloning. [Paper abstract](https://arxiv.org/abs/2302.06588).
- Personalized training: Van Le et al., ICCV 2023, Anti-DreamBooth. Authors report experiments with personalized diffusion generation. Results are limited to their experimental conditions. [Proceedings](https://openaccess.thecvf.com/content/ICCV2023/html/Van_Le_Anti-DreamBooth_Protecting_Users_from_Personalized_Text-to-image_Synthesis_ICCV_2023_paper.html).
- Image editing robustness: Bala et al., ICCV 2025, DCT-Shield. Authors report a favorable tradeoff between appearance and resistance to editing. Results are not proof of protection against identity cloning. [Proceedings](https://openaccess.thecvf.com/content/ICCV2025/html/Bala_DCT-Shield_A_Robust_Frequency_Domain_Defense_against_Malicious_Image_Editing_ICCV_2025_paper.html).
- Independent caution: Chen et al., AAAI 2026, Fragile by Design (published March 14, 2026). Authors report that evaluated personalized-generation defenses were fragile and sometimes visually detectable. This is significant contrary evidence, but it is not a universal finding about every other paper. [Proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/41170).

## Synthesis
Different studies address different tasks and do not share a common test distribution, hardware or outcome definition. No defensible overall ranking can be inferred. No evidence reviewed establishes six reliably ordered protection levels, a universal 60-second browser runtime, or effectiveness against the current ChatGPT image generator. Combining methods is an untested hypothesis, not an established improvement.

## Project decision
Retain the original question, do not declare a winning engine, and do not ship a protection claim. Research review can continue as a standalone contribution even if a deployable engine remains unestablished.
