package com.studly.network;

import com.octo.android.robospice.request.retrofit.RetrofitSpiceRequest;
import com.studly.model.StudlyEvent;

public class RequestJoinGroup extends RetrofitSpiceRequest<String, StudlyApi> {

    private StudlyEvent mEvent;
    private String mEmail;
    private boolean mJoin;
    
    public RequestJoinGroup(StudlyEvent event, String email, boolean join) {
        super(String.class, StudlyApi.class);
        mEvent = event;
        mEmail = email;
        mJoin = join;
    }

    @Override
    public String loadDataFromNetwork() throws Exception {
        //return getService().joinGroup(mEvent.getName(), mEmail, Boolean.toString(mJoin));
        return "OK";
    }

}
