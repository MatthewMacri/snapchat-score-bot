# Contributing to SnapScore Pixel

Thank you for your interest in contributing! Here's how you can help.

## 🎯 How to Contribute

### Reporting Bugs

1. **Check existing issues** first - maybe someone already reported it
2. **Take a screenshot** if the bot fails:
   ```bash
   adb exec-out screencap -p > bug_screenshot.png
   ```
3. **Open an issue** with:
   - Description of what happened
   - Your phone model
   - Snapchat version
   - Screenshot
   - Steps to reproduce
   - Expected vs actual behavior

### Suggesting Features

- Open an issue with tag `[FEATURE REQUEST]`
- Describe the feature and why it would help
- Give examples of how it would be used

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly:**
   ```bash
   python snapscore.py 10  # Test with 10 rounds
   ```
5. **Commit with clear messages:**
   ```bash
   git commit -m "Add feature: clear description of what changed"
   ```
6. **Push and create a Pull Request**

## 📋 Code Standards

- **Python 3.8+** compatibility
- **Comments** for complex logic
- **No external dependencies** unless absolutely necessary
- **Test on real hardware** before submitting
- **ADB safety** - never execute unsanitized commands

## 🔍 Testing Checklist

Before submitting a PR:

- [ ] Tested on actual Android device
- [ ] Ran at least 10 consecutive cycles
- [ ] Verified logging works (`snapscore_log.csv`)
- [ ] Checked pixel verification still works
- [ ] No breaking changes to existing features
- [ ] Code is commented where needed

## 🎨 Areas We Need Help

- **Coordinate calibration for other phones**
  - Pixel 6, 6a, 6 Pro
  - Samsung Galaxy S series
  - OnePlus
  - Other Androids

- **New features**
  - Multi-account support
  - Better image recognition for buttons
  - Scheduling improvements
  - Performance optimizations

- **Documentation**
  - Add guides for other phone models
  - Improve troubleshooting section
  - Create setup videos (optional)

- **Testing**
  - Long-term stability testing
  - Different Snapchat versions
  - Edge case handling

## 💡 Development Tips

### Setting up Dev Environment

```bash
git clone https://github.com/YOUR_USERNAME/snapchat-score-bot.git
cd snapchat-score-bot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Debugging

Enable ADB trace:
```bash
adb shell setprop log.tag.adb DEBUG
```

Get a screenshot:
```bash
adb exec-out screencap -p > screenshot.png
```

Test coordinate tapping:
```bash
adb shell input touchscreen tap 100 100
```

### Measuring New Coordinates

1. Take a screenshot
2. Open in image viewer
3. Hover over button to see coordinates
4. Update `snapscore.py` with new coordinates
5. Test with 5-10 test cycles

## 📝 Commit Message Format

```
[Type] Brief description (max 70 chars)

Longer explanation of what changed and why (optional).

Type should be one of:
- [FIX] - Bug fix
- [FEATURE] - New feature
- [IMPROVE] - Performance or code quality improvement
- [DOCS] - Documentation
- [TEST] - Testing
```

Examples:
```
[FIX] Select All button coordinates for Pixel 7
[FEATURE] Support for Samsung Galaxy S23
[IMPROVE] Faster screenshot processing
[DOCS] Add troubleshooting guide
```

## ⚠️ Important Notes

- **Account Safety:** Always warn users about ToS violations
- **Phone Safety:** Never tap dangerous coordinates without verification
- **Reversibility:** Make changes that can be easily reverted
- **Testing:** Test on actual devices before pushing

## 🚀 Release Process

(For maintainers)

1. Test all changes thoroughly
2. Update version in comments if needed
3. Update README with changes
4. Create release notes
5. Tag version: `git tag -a v1.0 -m "Release 1.0"`
6. Push tags: `git push origin --tags`

## 💬 Questions?

- Open an issue with `[QUESTION]` tag
- Check existing issues for answers
- Read README thoroughly first

## 🙏 Thank You

Every contribution matters! Your help makes SnapScore better for everyone.

Happy coding! 🎉
