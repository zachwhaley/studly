package com.studly.activity;

import android.app.ListActivity;
import android.os.Bundle;
import android.util.Log;

import com.studly.adapter.StudlyAdapter;
import com.studly.network.RequestStudlyEvents;

public class MainActivity extends ListActivity {

    private static final String TAG = "MainActivity";

    private RequestStudlyEvents mRequestStudlyEvents;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mRequestStudlyEvents = new RequestStudlyEvents();
        try {
            Log.d(TAG, "Setting list adapter");
            setListAdapter(new StudlyAdapter(this, mRequestStudlyEvents.loadDataFromNetwork()));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
