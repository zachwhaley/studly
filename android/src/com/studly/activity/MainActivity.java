package com.studly.activity;

import java.util.Comparator;

import android.accounts.Account;
import android.app.Dialog;
import android.app.DialogFragment;
import android.app.ListActivity;
import android.content.Context;
import android.content.IntentSender;
import android.location.Location;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesClient;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.location.LocationClient;
import com.octo.android.robospice.SpiceManager;
import com.octo.android.robospice.persistence.exception.SpiceException;
import com.octo.android.robospice.request.listener.RequestListener;
import com.studly.R;
import com.studly.fragment.ChooseAccountFragment;
import com.studly.fragment.ChooseAccountFragment.ChooseAccountListener;
import com.studly.fragment.ChooseGroupFragment;
import com.studly.fragment.ChooseGroupFragment.ChooseGroupListener;
import com.studly.model.StudlyMapping;
import com.studly.network.RequestStudlyGroups;
import com.studly.service.StudlyService;
import com.studly.util.AccountUtils;

public class MainActivity extends ListActivity implements ChooseAccountListener, ChooseGroupListener,
        GooglePlayServicesClient.ConnectionCallbacks, GooglePlayServicesClient.OnConnectionFailedListener {

    private static final String TAG = "MainActivity";
    private static final String CHOOSE_ACCOUNT_TAG = "account_chooser";
    private static final String CHOOSE_EVENT_TAG = "event_chooser";
    private static final String KEY_CHOSEN_ACCOUNT = "chosen_account";
    /*
     * Define a request code to send to Google Play services This code is
     * returned in Activity.onActivityResult
     */
    private final static int CONNECTION_FAILURE_RESOLUTION_REQUEST = 9000;

    /* Attributes */

    private SpiceManager mSpiceManager = new SpiceManager(StudlyService.class);
    private String mAccountName;
    private RequestStudlyGroups mRequestStudlyGroups;
    private StudlyAdapter mStudlyAdapter;

    private boolean mConnected = false;
    private LocationClient mLocationClient;

    /* Methods */

    private void startLocationClient() {
        // Connect the client.
        mLocationClient.connect();
    }

    private void stopLocationClient() {
        // Disconnecting the client invalidates it.
        mLocationClient.disconnect();
    }

    public Location getLocation() {
        return mConnected ? mLocationClient.getLastLocation() : null;
    }

    private void performRequest() {
        mSpiceManager.execute(mRequestStudlyGroups, new StudlyMappingRequestListener());
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (!AccountUtils.isAuthenticated(this)) {
            ChooseAccountFragment.newInstance(this).show(getFragmentManager(), CHOOSE_ACCOUNT_TAG);
        }

        if (savedInstanceState != null) {
            mAccountName = savedInstanceState.getString(KEY_CHOSEN_ACCOUNT);
        } else {
            mAccountName = AccountUtils.getChosenAccountName(this);
        }

        /*
         * Create a new location client, using the enclosing class to handle
         * callbacks.
         */
        mLocationClient = new LocationClient(this, this, this);

        mRequestStudlyGroups = new RequestStudlyGroups();
        try {
            Log.d(TAG, "Setting list adapter");
            performRequest();
            setListAdapter(mStudlyAdapter);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
        case R.id.action_new_event:
            ChooseGroupFragment.newInstance(this).show(getFragmentManager(), CHOOSE_EVENT_TAG);
            return true;
        default:
            return super.onOptionsItemSelected(item);
        }
    }

    @Override
    protected void onStart() {
        super.onStart();
        startLocationClient();
        mSpiceManager.start(this);
    }

    @Override
    protected void onStop() {
        stopLocationClient();
        mSpiceManager.shouldStop();
        super.onStop();
    }

    @Override
    public void onConnected(Bundle dataBundle) {
        mConnected = true;
    }

    @Override
    public void onDisconnected() {
        mConnected = false;
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        if (mAccountName != null) {
            outState.putString(KEY_CHOSEN_ACCOUNT, mAccountName);
        }
        super.onSaveInstanceState(outState);
    }

    @Override
    public void onAccountChosen(Account account) {
        AccountUtils.setChosenAccountName(this, account.name);
    }

    @Override
    public void onGroupChosen(long calId) {
        Toast.makeText(this, "Event title " + calId, Toast.LENGTH_SHORT).show();
    }

    /* Classes */

    private class StudlyAdapter extends ArrayAdapter<StudlyMapping> {

        public StudlyAdapter(Context context, StudlyMapping.List events) {
            super(context, 0, events);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            Log.d(TAG, "Create new view");
            LayoutInflater inflater = getLayoutInflater();
            View view = inflater.inflate(android.R.layout.simple_list_item_1, null);

            final StudlyMapping mapping = getItem(position);
            if (mapping != null) {
                Log.d(TAG, "creating row for event " + mapping.getTitle() + " calendar " + mapping.getCalendarId());

                TextView textView = (TextView) view.findViewById(android.R.id.text1);
                textView.setText(mapping.getTitle());
            }
            return view;
        }

    }

    private class StudlyMappingRequestListener implements RequestListener<StudlyMapping.List> {

        @Override
        public void onRequestFailure(SpiceException spiceException) {
        }

        @Override
        public void onRequestSuccess(StudlyMapping.List mappings) {
            mStudlyAdapter = new StudlyAdapter(MainActivity.this, mappings);
            mStudlyAdapter.sort(new Comparator<StudlyMapping>() {
                @Override
                public int compare(StudlyMapping lhs, StudlyMapping rhs) {
                    final Location loc = MainActivity.this.getLocation();

                    Location lhsLoc = new Location("");
                    lhsLoc.setLatitude(lhs.getLatitude());
                    lhsLoc.setLongitude(lhs.getLongitude());
                    Log.d(TAG, "lhs lat " + lhsLoc.getLatitude() + " lon " + lhsLoc.getLongitude());

                    Location rhsLoc = new Location("");
                    rhsLoc.setLatitude(rhs.getLatitude());
                    rhsLoc.setLongitude(rhs.getLongitude());
                    Log.d(TAG, "rhs lat " + rhsLoc.getLatitude() + " lon " + rhsLoc.getLongitude());

                    float rhsDist = loc.distanceTo(rhsLoc);
                    float lhsDist = loc.distanceTo(lhsLoc);

                    Log.d(TAG, "rhs dist " + rhsDist + " lhs dist " + lhsDist);
                    return (int) (lhsDist - rhsDist);
                }
            });
            setListAdapter(mStudlyAdapter);
        }

    }

    /*
     * Called by Location Services if the attempt to Location Services fails.
     */
    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        /*
         * Google Play services can resolve some errors it detects. If the error
         * has a resolution, try sending an Intent to start a Google Play
         * services activity that can resolve error.
         */
        if (connectionResult.hasResolution()) {
            try {
                // Start an Activity that tries to resolve the error
                connectionResult.startResolutionForResult(this, CONNECTION_FAILURE_RESOLUTION_REQUEST);
                /*
                 * Thrown if Google Play services canceled the original
                 * PendingIntent
                 */
            } catch (IntentSender.SendIntentException e) {
                // Log the error
                e.printStackTrace();
            }
        } else {
            /*
             * If no resolution is available, display a dialog to the user with
             * the error.
             */
            // Get the error code
            int errorCode = connectionResult.getErrorCode();
            // Get the error dialog from Google Play services
            Dialog errorDialog = GooglePlayServicesUtil.getErrorDialog(errorCode, this,
                    CONNECTION_FAILURE_RESOLUTION_REQUEST);
            // If Google Play services can provide an error dialog
            if (errorDialog != null) {
                // Create a new DialogFragment for the error dialog
                ErrorDialogFragment errorFragment = new ErrorDialogFragment();
                // Set the dialog in the DialogFragment
                errorFragment.setDialog(errorDialog);
                // Show the error dialog in the DialogFragment
                errorFragment.show(getFragmentManager(), "Location Updates");
            }
        }
    }

    // Define a DialogFragment that displays the error dialog
    public static class ErrorDialogFragment extends DialogFragment {
        // Global field to contain the error dialog
        private Dialog mDialog;

        // Default constructor. Sets the dialog field to null
        public ErrorDialogFragment() {
            super();
            mDialog = null;
        }

        // Set the dialog to display
        public void setDialog(Dialog dialog) {
            mDialog = dialog;
        }

        // Return a Dialog to the DialogFragment.
        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            return mDialog;
        }
    }

}
