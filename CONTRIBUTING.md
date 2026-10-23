# Contributing to SnapScore Pixel

Thanks for your interest in contributing. Here's how you can help.

## Reporting Bugs

1. Check existing issues first
2. Take a screenshot if the bot fails: `adb exec-out screencap -p > bug_screenshot.png`
3. Open an issue with:
   - Description of what happened
   - Your phone model
   - Snapchat version
   - Steps to reproduce
   - Expected vs actual behavior

## Suggesting Features

Open an issue describing:
- What feature you'd like to see
- Why it would be useful
- How it would work

## Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly: `python snapscore.py 10`
5. Commit with clear messages
6. Push and create a Pull Request

## Code Standards

- Python 3.8+ compatibility
- Comments for complex logic
- Test on real hardware before submitting
- Keep security in mind (ADB safety)
- No unnecessary external dependencies

## Testing Checklist

Before submitting a PR:
- Tested on actual Android device
- Ran at least 10 consecutive cycles
- Verified logging works
- Checked pixel verification still works
- No breaking changes

## Areas Needing Help

- Support for other Android phones (Galaxy, OnePlus, etc)
- Image recognition for button detection
- Multi-account support
- Documentation improvements
- Long-term stability testing

## Development Tips

Get a screenshot:
```bash
adb exec-out screencap -p > screenshot.png
```

Test a specific coordinate:
```bash
adb shell input touchscreen tap 100 100
```

Measure coordinates:
1. Take a screenshot
2. Open in image viewer
3. Hover to see coordinates
4. Update snapscore.py constants
5. Test with 5-10 cycles

## Commit Message Format

```
[Type] Brief description

Longer explanation (optional)

Types: [FIX], [FEATURE], [IMPROVE], [DOCS], [TEST]
```

Examples:
```
[FIX] Fix Select All button coordinates for Pixel 7
[FEATURE] Add support for Samsung Galaxy S23
[IMPROVE] Faster screenshot processing
[DOCS] Add troubleshooting guide
```

## Important Notes

- Account Safety: Always warn about ToS violations
- Phone Safety: Never tap dangerous coordinates without verification
- Testing: Test on actual devices before pushing
- Reversibility: Make changes that can be easily reverted

## Questions?

Open an issue with [QUESTION] tag or check existing documentation.

Thanks for helping make SnapScore better!
