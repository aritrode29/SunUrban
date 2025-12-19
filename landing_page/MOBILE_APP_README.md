# SunUrban Mobile App (PWA)

This is a Progressive Web App (PWA) that can be installed on mobile devices, similar to native apps like Sunrun's mobile app.

## Features

✅ **Installable** - Can be installed on iOS and Android devices  
✅ **Offline Support** - Works offline with cached content  
✅ **App-like Experience** - Full-screen, standalone mode  
✅ **Push Notifications Ready** - Infrastructure for future notifications  
✅ **Fast Loading** - Service worker caching for instant loads  

## How to Install

### On Android (Chrome)

1. Visit https://aritrode29.github.io/SunUrban/ on your Android device
2. Tap the menu (three dots) in Chrome
3. Select "Add to Home screen" or "Install app"
4. Confirm installation
5. The app will appear on your home screen

### On iOS (Safari)

1. Visit https://aritrode29.github.io/SunUrban/ on your iPhone/iPad
2. Tap the Share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Customize the name if desired
5. Tap "Add"
6. The app will appear on your home screen

### On Desktop (Chrome/Edge)

1. Visit https://aritrode29.github.io/SunUrban/
2. Look for the install icon in the address bar
3. Click "Install" when prompted
4. The app will open in its own window

## App Icons

The app needs icons to display properly. To generate them:

1. Open `generate-icons.html` in a browser
2. Click "Generate Icons"
3. Download both icon sizes (192x192 and 512x512)
4. Save them as `icon-192.png` and `icon-512.png` in the `landing_page` folder

Alternatively, you can create custom icons:
- **Size**: 192x192 and 512x512 pixels
- **Format**: PNG with transparency
- **Design**: Should include the SunUrban logo/sun icon
- **Background**: Orange gradient (#FF6B35 to #FF8C42)

## Technical Details

### Files

- `manifest.json` - PWA configuration
- `sw.js` - Service worker for offline functionality
- `icon-192.png` - App icon (192x192)
- `icon-512.png` - App icon (512x512)

### Service Worker

The service worker (`sw.js`) handles:
- Caching static assets for offline access
- Background sync for form submissions
- Update notifications when new version is available

### Manifest

The manifest (`manifest.json`) defines:
- App name and description
- Icons and splash screens
- Display mode (standalone)
- Theme colors
- App shortcuts

## Testing

### Test Installation

1. Open the site in Chrome DevTools
2. Go to Application tab
3. Check "Service Workers" - should show registered
4. Check "Manifest" - should show all details
5. Check "Lighthouse" - run PWA audit

### Test Offline

1. Open DevTools → Network tab
2. Enable "Offline" mode
3. Refresh the page
4. Site should still load from cache

## Updates

When you update the app:
1. Update the version in `sw.js` (CACHE_NAME)
2. Push changes to GitHub
3. Users will see an update notification
4. They can refresh to get the latest version

## Browser Support

- ✅ Chrome/Edge (Android & Desktop)
- ✅ Safari (iOS 11.3+)
- ✅ Firefox (Android & Desktop)
- ✅ Samsung Internet

## Comparison to Sunrun App

Like Sunrun's mobile app, this PWA provides:
- **Quote Requests** - Easy form submission
- **Project Information** - All details accessible
- **Offline Access** - View content without internet
- **Installation** - Add to home screen
- **Fast Performance** - Cached assets load instantly

## Future Enhancements

Potential features to add:
- Push notifications for project updates
- Background sync for form submissions
- Geolocation for site finder
- Camera integration for site photos
- Biometric authentication
- Dark mode support

## Troubleshooting

### App won't install
- Ensure you're using HTTPS (required for PWA)
- Check that manifest.json is accessible
- Verify service worker is registered
- Clear browser cache and try again

### Offline mode not working
- Check service worker registration in DevTools
- Verify sw.js is in the root directory
- Check browser console for errors

### Icons not showing
- Ensure icon files exist (icon-192.png, icon-512.png)
- Check file paths in manifest.json
- Verify icons are PNG format

## Support

For issues or questions:
- Check browser console for errors
- Verify all files are deployed correctly
- Test in different browsers
- Check GitHub Actions deployment status

